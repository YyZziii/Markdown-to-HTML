from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def simple_markdown_to_html(md_text):
    html = []
    lines = md_text.split('\n')
    in_ul = False
    in_ol = False
    in_blockquote = False
    blockquote_lines = []
    in_code_block = False
    code_block_content = []
    code_block_lang = ''
    in_table = False
    table_rows = []
    for i, line in enumerate(lines):
        orig_line = line
        line = line.rstrip()
        # HTML brut
        if re.match(r'^\s*<.+?>', line):
            html.append(line)
            continue
        # Bloc de code avec langage
        code_block_start = re.match(r'^```(\w*)', line.strip())
        if code_block_start:
            if not in_code_block:
                in_code_block = True
                code_block_content = []
                code_block_lang = code_block_start.group(1)
                continue
            else:
                in_code_block = False
                lang_class = f' class="language-{code_block_lang}"' if code_block_lang else ''
                html.append(f'<pre><code{lang_class}>{'\n'.join(code_block_content)}</code></pre>')
                code_block_lang = ''
                continue
        if in_code_block:
            code_block_content.append(orig_line)
            continue
        # Séparateur horizontal
        if re.match(r'^\s*([-*_]){3,}\s*$', line):
            html.append('<hr>')
            continue
        # Titres alternatifs
        if i+1 < len(lines):
            if re.match(r'^[=]{3,}\s*$', lines[i+1]):
                html.append(f'<h1>{line}</h1>')
                continue
            if re.match(r'^[-]{3,}\s*$', lines[i+1]):
                html.append(f'<h2>{line}</h2>')
                continue
        # Titres (avec ou sans espace)
        m = re.match(r'^(#{1,6}) ?(.*)', line)
        if m:
            level = len(m.group(1))
            content = m.group(2)
            html.append(f'<h{level}>{content}</h{level}>')
            continue
        # Citations multi-paragraphes
        if line.startswith('>') or (in_blockquote and line.strip() == ''):
            if not in_blockquote:
                in_blockquote = True
                blockquote_lines = []
            if line.startswith('>'):
                blockquote_lines.append(line[1:].lstrip())
            else:
                blockquote_lines.append('')
            # Si c'est la dernière ligne ou la prochaine ligne n'est pas une citation
            if i+1 == len(lines) or (not lines[i+1].startswith('>') and lines[i+1].strip() != ''):
                # On ferme le blockquote
                html.append('<blockquote>')
                # Découpe en paragraphes
                paragraph = []
                for l in blockquote_lines + ['']:
                    if l == '':
                        if paragraph:
                            html.append('<p>' + '<br>'.join(paragraph).strip() + '</p>')
                            paragraph = []
                    else:
                        paragraph.append(l)
                html.append('</blockquote>')
                in_blockquote = False
                blockquote_lines = []
            continue
        else:
            if in_blockquote:
                # On ferme le blockquote si on sort de la citation
                html.append('<blockquote>')
                paragraph = []
                for l in blockquote_lines + ['']:
                    if l == '':
                        if paragraph:
                            html.append('<p>' + '<br>'.join(paragraph).strip() + '</p>')
                            paragraph = []
                    else:
                        paragraph.append(l)
                html.append('</blockquote>')
                in_blockquote = False
                blockquote_lines = []
        # Tableaux
        if '|' in line and re.match(r'^\s*\|.*\|\s*$', line):
            table_rows.append(line)
            if not in_table:
                in_table = True
            if i+1 == len(lines) or not ('|' in lines[i+1]):
                # Fin du tableau
                html.append('<table>')
                for idx, row in enumerate(table_rows):
                    cols = [c.strip() for c in row.strip('|').split('|')]
                    tag = 'th' if idx == 0 else 'td'
                    html.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cols) + '</tr>')
                html.append('</table>')
                table_rows = []
                in_table = False
            continue
        # Listes de tâches
        m = re.match(r'^[-*+] \[( |x|X)\] (.*)', line)
        if m:
            checked = 'checked' if m.group(1).lower() == 'x' else ''
            if not in_ul:
                html.append('<ul>')
                in_ul = True
            html.append(f'<li><input type="checkbox" disabled {checked}> {m.group(2)}</li>')
            continue
        # Listes imbriquées (niveau 2)
        m = re.match(r'^  [-*+] (.*)', line)
        if m and in_ul:
            html[-1] = html[-1][:-5] + '<ul><li>' + m.group(1) + '</li></ul></li>'
            continue
        # Listes à puces
        if re.match(r'^[-*+] ', line):
            if not in_ul:
                html.append('<ul>')
                in_ul = True
            html.append(f'<li>{line[2:]}</li>')
            continue
        else:
            if in_ul:
                html.append('</ul>')
                in_ul = False
        # Listes numérotées
        m = re.match(r'^(\d+)\. (.*)', line)
        if m:
            if not in_ol:
                html.append('<ol>')
                in_ol = True
            html.append(f'<li>{m.group(2)}</li>')
            continue
        else:
            if in_ol:
                html.append('</ol>')
                in_ol = False
        # Images
        line = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img alt="\1" src="\2" />', line)
        # Liens
        line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
        # Gras
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'__(.+?)__', r'<strong>\1</strong>', line)
        # Italique
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
        line = re.sub(r'_(.+?)_', r'<em>\1</em>', line)
        # Code inline
        line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
        # Saut de ligne forcé
        if line.endswith('  '):
            line = line.rstrip() + '<br>'
        # Paragraphe
        if line.strip() != '':
            html.append(f'<p>{line}</p>')
    if in_ul:
        html.append('</ul>')
    if in_ol:
        html.append('</ol>')
    if in_blockquote:
        html.append('<blockquote>')
        paragraph = []
        for l in blockquote_lines + ['']:
            if l == '':
                if paragraph:
                    html.append('<p>' + '<br>'.join(paragraph).strip() + '</p>')
                    paragraph = []
            else:
                paragraph.append(l)
        html.append('</blockquote>')
    return '\n'.join(html)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_markdown():
    data = request.get_json()
    md_text = data.get('markdown', '')
    html = simple_markdown_to_html(md_text)
    return jsonify({'html': html})

if __name__ == '__main__':
    app.run(debug=True) 