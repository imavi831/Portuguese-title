# title_formatter.py
import re
# Gradio will be imported if the UI is launched.
import gradio as gr

# --- DATA (CONSTANTS) ---
KEYWORDS = {
    'o', 'a', 'os', 'uma', 'umas', 'as', 'ao', 'aos', 'um', 'uns', 'às', 'à',
    'me', 'te', 'se', 'lhe', 'nos', 'vos', 'que', 'e', 'ou', 'com',
    'em', 'por', 'no', 'na', 'nas', 'mas', 'para', 'pelo', 'pelos',
    'pela', 'pelas', 'sob', 'sobre', 'nem', 'entre', 'sem', 'de', 'do',
    'da', 'dos', 'das'
}

# This is the new, comprehensive list of censored words, converted to a lowercase set for efficient lookups.
CENSORED_WORDS_SET = {
    "adolescente", "adolescentes", "afeminado", "afeminados", "arromba", "arrombada",
    "arrombado", "arrombam", "arrombar", "bacanal", "bacanais", "benga", "bengas",
    "bicha", "bichas", "boceta", "bocetas", "bocetinha", "bocetinhas", "bocetuda",
    "bocetudas", "boiola", "boiolas", "boiolinha", "boiolinhas", "boquete",
    "boqueteira", "boqueteiras", "boqueteiro", "boqueteiros", "boquetes", "bosta",
    "bostas", "bostinha", "bostinhas", "brioco", "briocos", "bucetinha",
    "bucetinhas", "bucetuda", "bucetudas", "bunda", "bundão", "bundas", "bundões",
    "bunduda", "bundudas", "bundudo", "bundudos", "cabaço", "cacete", "cacetão",
    "cacetes", "cacetinho", "cacetinhos", "cachorra", "cachorras", "cachorrinha",
    "cachorrona", "cadela", "cadelas", "cadelinha", "cadelinhas", "caralhão",
    "caralhões", "caralhinho", "caralhinhos", "caralho", "caralhos", "caralhudo",
    "caralhudos", "chifre", "chifres", "chifruda", "chifrudas", "chifrudo",
    "chifrudos", "chupa", "chupada", "chupadinho", "chupadinha", "chupado",
    "chupam", "chuparam", "chuparão", "chupar", "chupeta", "chupetas", "chupetinha",
    "chupetinhas", "colegial", "colegiais", "come", "comem", "comendo", "comer",
    "comi", "corna", "cornas", "cornear", "corneada", "corneado", "corno", "cornos",
    "cornuda", "cornudas", "cornudo", "cornudos", "criança", "crianças", "cu",
    "cus", "cú", "cuzão", "cuzões", "cuzinho", "cuzinhos", "cuzona", "cuzonas",
    "d.i.l.f.s", "decabaçam", "descabaçar", "dilfs", "ejacular", "ejaculada",
    "ejaculadas", "ejaculado", "ejaculados", "ejaculando", "ejacularam", "enrabar",
    "enrabam", "enrabaram", "esperma", "espermas", "espermatozóide",
    "espermatozóides", "esporrada", "esporradas", "esporrado", "esporrados",
    "esporrar", "filho da mãe", "filho da puta", "foda", "fodas", "foder",
    "foderam", "fodem", "fodida", "fodidas", "fodido", "fodidos", "fodilhão",
    "fodilhona", "fudeu", "fuder", "fuderam", "fudida", "fudidas", "fudido",
    "fudidos", "gang bang", "garganta profunda", "garota", "garotas", "garoto",
    "garotos", "goza", "gozada", "gozado", "gozam", "gozaram", "gozarão", "gozar",
    "gozo", "grelo", "grelos", "japa", "japas", "japinha", "japinhas", "jorrar",
    "jorrando", "leite", "leitinho", "lolita", "lolitas", "lolitinha", "lolitinhas",
    "m.i.l.f.s", "mamada", "mamam", "mamar", "mamaram", "mastro", "mastros", "merda",
    "merdas", "merdinha", "merdinhas", "metem", "meter", "metendo", "mete",
    "mijada", "mijadas", "mijado", "mijados", "mijar", "mijo", "mijos", "milfs",
    "mulata", "mulatas", "mulatinha", "mulatinhas", "mulatinho", "mulatinhos",
    "mulato", "mulatos", "negão", "negões", "negona", "negonas", "neguinha",
    "neguinhas", "neguinho", "neguinhos", "negro", "ninfeta", "ninfetas",
    "ninfetinha", "ninfetinhas", "novinha", "novinhas", "novinho", "novinhos",
    "orgia", "orgias", "pau", "paus", "pauzão", "pauzões", "pauzudo", "pauzudos",
    "peitão", "peitões", "peitinho", "peitinhos", "peito", "peitos", "peituda",
    "peitudas", "pênis", "pica", "picas", "pintão", "pintões", "pintinho",
    "pintinhos", "pinto", "pintos", "pintudo", "pintudos", "piranha", "piranhas",
    "piriguete", "piriguetes", "piroca", "pirocada", "pirocadas", "pirocas",
    "pirocudo", "pirocudos", "piroquinha", "piroquinhas", "popozão", "popozões",
    "popozuda", "popozudas", "porra", "porras", "preta", "pretas", "pretinha",
    "pretinhas", "pretinho", "pretinhos", "preto", "punheta", "punhetas",
    "punheteiro", "punheteiros", "punhetinha", "punhetinhas", "puta", "puta merda",
    "putaria", "putarias", "putas", "putinha", "putinhas", "putona", "putonas",
    "raba", "rabas", "rabeta", "rabetas", "rabinho", "rabinhos", "rabo", "rabos",
    "rabuda", "rabudas", "rapariga", "raparigas", "rasgada", "rasgadas", "rola",
    "rolão", "rolões", "rolas", "rolinha", "rolinhas", "roludo", "sapata",
    "sapatão", "sapatões", "sêmen", "surpresa cremosa", "suruba", "surubão",
    "surubas", "surubinha", "surubinhas", "surubona", "tcheca", "tchecona",
    "tcheconas", "tchequinha", "tchequinhas", "teta", "tetão", "tetões", "tetas",
    "tetinha", "tetinhas", "tetuda", "tetutas", "toba", "tobas", "tora", "toras",
    "trava", "travas", "traveco", "travecos", "trepa", "trepada", "trepam",
    "trepando", "trepar", "vadia", "vadias", "vagabunda", "vagabundas", "vara",
    "varas", "varões", "velcro", "velcros", "viadinho", "viadinhos", "viado",
    "viados", "xana", "xanas", "xaninha", "xaninhas", "xavasca", "xavascas",
    "xavasquinha", "xavasquinhas", "xoxota", "xoxotas", "xoxotinha", "xoxotona",
    "xoxotonas", "xoxotinhas"
}

# --- CORE LOGIC FUNCTIONS ---
def _capitalize_word_part(part_str):
    if not part_str:
        return ""
    if len(part_str) == 1:
        return part_str.upper()
    return part_str[0].upper() + part_str[1:].lower()

def censor_word_if_needed(original_word_token, censored_set_to_use):
    if not original_word_token or not original_word_token.strip():
        return original_word_token

    start_alpha_idx = -1
    end_alpha_idx = -1
    first_alpha_char_original_case = None

    for i, char_val in enumerate(original_word_token):
        if char_val.isalpha():
            if start_alpha_idx == -1:
                start_alpha_idx = i
                first_alpha_char_original_case = char_val
            end_alpha_idx = i

    if start_alpha_idx == -1:
        return original_word_token

    prefix = original_word_token[:start_alpha_idx]
    core_original_case_word = original_word_token[start_alpha_idx : end_alpha_idx+1]
    suffix = original_word_token[end_alpha_idx+1:]
    core_lower = core_original_case_word.lower()

    word_to_use_for_rule_lookup = None
    derived_is_plural = False

    if len(core_lower) > 1 and core_lower.endswith('s'):
        singular_form = core_lower[:-1]
        if singular_form in censored_set_to_use:
            word_to_use_for_rule_lookup = singular_form
            derived_is_plural = True

    if word_to_use_for_rule_lookup is None:
        if core_lower in censored_set_to_use:
            word_to_use_for_rule_lookup = core_lower
        else:
            return original_word_token

    # *** LOGIC CORRECTION STARTS HERE ***

    L = len(word_to_use_for_rule_lookup)
    first_char_for_output = first_alpha_char_original_case
    censored_core_structure = ""
    
    # Determine the last character based on whether the word is plural
    last_char_for_output = ""
    if L >= 3: # Words of length 3+ have a last letter component
        if derived_is_plural:
            last_char_for_output = "s"
        else:
            last_char_for_output = word_to_use_for_rule_lookup[-1]

    # Build the censored word structure
    if L < 2:
        return original_word_token # Rules don't apply to 1-letter words

    if L == 2: # e.g., Cu -> C. or Cus -> C.s
        periods = "."
        censored_core_structure = first_char_for_output + periods
        if derived_is_plural:
            censored_core_structure += "s"
    elif L >= 3:
        if L == 3: periods = "."
        elif L == 4: periods = ".."
        else: periods = "..." # L >= 5
        censored_core_structure = first_char_for_output + periods + last_char_for_output
    
    # If for some reason no structure was built, return original
    if not censored_core_structure:
        return original_word_token

    return prefix + censored_core_structure + suffix


def standardize_major_separators(title_line):
    separator_pattern = re.compile(r"\s+[:\-]\s+")
    parts = separator_pattern.split(title_line)
    num_actual_separators = len(parts) - 1
    if num_actual_separators <= 0: return title_line
    if num_actual_separators == 1: return f"{parts[0].strip()} - {parts[1].strip()}"
    reconstructed_title = parts[0].strip() + ": " + parts[1].strip()
    for i in range(2, len(parts)): reconstructed_title += f" - {parts[i].strip()}"
    return reconstructed_title

def apply_capitalization_rules_to_line(line_text_with_std_separators, current_censored_words_set):
    if not line_text_with_std_separators.strip(): return line_text_with_std_separators
    words = line_text_with_std_separators.split(' ')
    processed_words = []
    capitalize_next_word_override = True
    for original_token in words:
        if not original_token:
            processed_words.append(original_token)
            continue
        is_standalone_hyphen_separator = (original_token == "-")
        processed_word_for_token = ""
        if is_standalone_hyphen_separator:
            processed_word_for_token = original_token
        elif not is_standalone_hyphen_separator and '-' in original_token:
            parts = original_token.split('-')
            processed_parts = [ _capitalize_word_part(censor_word_if_needed(p, current_censored_words_set)) for p in parts ]
            processed_word_for_token = '-'.join(processed_parts)
        else:
            word_after_censorship = censor_word_if_needed(original_token, current_censored_words_set)
            original_token_lower = original_token.lower()
            is_keyword_and_not_censored = (original_token_lower in KEYWORDS and word_after_censorship == original_token)
            if capitalize_next_word_override:
                processed_word_for_token = _capitalize_word_part(word_after_censorship)
            elif is_keyword_and_not_censored:
                processed_word_for_token = original_token_lower
            else:
                processed_word_for_token = _capitalize_word_part(word_after_censorship)
        processed_words.append(processed_word_for_token)
        if is_standalone_hyphen_separator or original_token.endswith(":"):
            capitalize_next_word_override = True
        else:
            capitalize_next_word_override = False
    return ' '.join(processed_words)

def format_title_line(line_text, current_censored_words_set_to_use=None):
    """Processes a single line of text with all formatting rules."""
    if current_censored_words_set_to_use is None:
        current_censored_words_set_to_use = CENSORED_WORDS_SET
    if not line_text or not line_text.strip(): return line_text
    line_with_std_separators = standardize_major_separators(line_text)
    final_line = apply_capitalization_rules_to_line(line_with_std_separators, current_censored_words_set_to_use)
    return final_line

def format_multiline_title(multiline_text, current_censored_words_set_to_use=None):
    """Main public function to format multiline text."""
    if current_censored_words_set_to_use is None:
        current_censored_words_set_to_use = CENSORED_WORDS_SET
    if not multiline_text: return ""
    lines = multiline_text.split("\n")
    new_lines = [format_title_line(l, current_censored_words_set_to_use) for l in lines]
    return "\n".join(new_lines)

# --- GRADIO UI FUNCTION ---
def create_gradio_interface():
    """Creates and returns the Gradio interface for the title formatter."""
    iface = gr.Interface(
        fn=format_multiline_title, # Uses the main formatting function
        inputs=gr.Textbox(lines=10, placeholder="Enter your text here...", label="Input Text"),
        outputs=gr.Textbox(label="Formatted Text"),
        title="Advanced Title Formatter (from GitHub)",
        description=(
            "Formats titles with capitalization, separator standardization, and word censorship.\n"
            "Censored words list is embedded. Censorship rules:\n"
            "- 2-letter (Cu): C. or C.s\n"
            "- 3-letter (Pau): P.u or P.us\n"
            "- 4-letter (Pica): P..a or P..as\n"
            "- 5+ letters (Boquete): B...e or B...es"
        ),
        examples=[
            ["Star Wars : Episodio V - o Imperio Contra-Ataca"],
            ["um titulo sobre pau e pica e os caralhos voadores"],
            ["cachorro-quente de CU com Boquete!"],
            ["As novinhas e suas picas"],
        ],
        allow_flagging='never'
    )
    return iface

# --- MAIN EXECUTION BLOCK (for standalone running) ---
if __name__ == "__main__":
    print("Title Formatter script running directly. Launching Gradio UI...")
    # In Colab, users should !pip install gradio first.
    formatter_app = create_gradio_interface()
    formatter_app.launch(debug=True) # Use share=True if you want a public link when running from Colab
