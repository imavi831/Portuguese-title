# title_formatter.py
import re
# Gradio will be imported if the UI is launched.
# We define it here for type hinting if needed, or it can be imported locally in create_gradio_interface.
import gradio as gr 

# --- DATA (CONSTANTS) ---
KEYWORDS = {
    'o', 'a', 'os', 'uma', 'umas', 'as', 'ao', 'aos', 'um', 'uns', 'às', 'à',
    'me', 'te', 'se', 'lhe', 'nos', 'vos', 'que', 'e', 'ou', 'com',
    'em', 'por', 'no', 'na', 'nas', 'mas', 'para', 'pelo', 'pelos',
    'pela', 'pelas', 'sob', 'nem', 'entre', 'sem', 'de', 'do',
    'da', 'dos', 'das'
}

CENSORED_WORDS_SET = {
    "adolescente", "adolescentes", "afeminado", "afeminados", "arromba", 
    "arrombado(a)", "arrombar", "ass (azz, assload, etc.)", "asshole,assload", 
    "bacanal", "bicha", "bichas", "bj", "blowjob,bj", "boceta", "bocetinha", 
    "bocetuda", "boiola", "boiolas", "boquete", "boqueteira", "boquetes", 
    "bosta", "bostas", "brioco", "buceta", "bucetinha", "bucetuda", "bullshit", 
    "bunda", "bundão", "bundas", "bundões", "bunduda", "cabaço", "cacete", 
    "cacetão", "cacetinho", "cachorra", "cachorras", "cachorrinha", "cadela", 
    "cadelas", "cadelinha", "caralh लहान", "caralhão", "caralhudo", "caralho", 
    "caralhos", "chifre", "chifruda", "chifrudo", "chink", "chupa", "chupada", 
    "chupam", "chupar", "chuparão", "chuparam", "chupeta", "chupetinha", "clit", 
    "cock", "cocksucker", "colegial", "come", "comendo", "comer", "comi", "corna", 
    "cornear", "corneado", "corno", "criança", "cu", "cú", "cum", "cunt", 
    "cuzinho", "d.i.l.f.(s)", "danada", "descabaçar", "desgraça", 
    "devassa", "dick", "dilf(s)", "ejaculado", "ejacular", "ejaculando", 
    "enrabar", "enrabaram", "esperma", "espermas", "espermatozóide", "esporrar", 
    "esporrado", "faggot", "falo", "farra", "filho da mãe", "filho da puta", 
    "foda", "fode", "foder", "foderam", "fodem", "fodido", "fodilhon", "fodil hona",
    "fogosa", "fuck (any version)", "fuder", "fudeu", "fudido", "gang bang", 
    "garganta profunda", "garoto", "garota", "Garotas", "gay", "gook", "goza", "gozado", 
    "gozam", "gozar", "gozarão", "gozo", "grelo", "grupal", "homem,homens maduro,maduros,experiente,experientes", 
    "homossexual", "japa", "japinha", "japonesa,", "jerk off", "jizz", "jorrar", 
    "jorrando", "krl", "leitinho, surpresa cremosa", "lésbica", "lolita", 
    "lolitas", "lolitinha", "m.i.l.f.(s)", "mamada", "mamar", "mastro", 
    "mastros", "masturbação", "meter", "mete", "metendo", "merda", "merdas", 
    "mijar", "mijado", "mijo", "milf(s)", "motherfucker", "mulata", 
    "mulatinho, mulatinha", "mulher, mulher jovem", "mulher,mulheres madura,maduras,experiente,experientes", 
    "nádegas, bumbum, traseiro", "negão", "negões", "negona", "negonas", "neguinho, neguinha", 
    "negro, negra", "negro, preto", "nigger", "ninfeta", "ninfetinha", "novinha", 
    "orgia", "orgias", "pau", "pauzão", "pauzudo", "peitão", 
    "peitinho", "peitinhos", "peito", "peituda", "penis", "pênis", "pica", 
    "picas", "pintão", "pinto", "pintos", "pintudo", "piranha", "piranhas", 
    "piriguete", "piroca", "pirocada", "pirocudo", "pirocas", 
    "piss,pissed,pissing", "popozão", "popozuda", "porra", "preto", 
    "pretinho, preta, pretinha", "punheta", "punheteiro", "punheteiro, punhetinha", 
    "pussy,pussies", "puta", "puta merda", "putaria", "putas", "putinha", 
    "putona", "rabo", "rabuda", "rabeta","Rabinho", "Rabinhos","rapariga", "raparigas", "rasgada", 
    "rasgadas", "rola", "rolas", "roludo", "safada", "sapata", "sapatão", 
    "screw", "seios", "semen", "sêmen", "sexo anal", "sexo grupal", "sexo oral", 
    "shit", "slut", "sperm", "spic", "squirt,er,ing", "suck", "suruba", 
    "surubão", "surubas", "surubona", "tcheca", "tchecona", "tchequinha", 
    "teta", "tetão", "tetas", "tetuda", "tirar a virgindade", "tit", "tits", 
    "titty", "toba", "tora", "traição, adultério", "traído", "transar", "trava", 
    "traveco", "trepa", "trepada", "trepando", "trepar", "twat", "vadia", 
    "vadias", "vagabunda", "vagabundas", "vagina", "vara", "velcro", "viadinho", 
    "viado", "virgem", "vsf", "whore", "xana", "xaninha", "xavasca", "xoxota", 
    "xoxotinha", "benga", "bem dotado"
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
    
    L = len(word_to_use_for_rule_lookup)
    first_char_for_output = first_alpha_char_original_case 
    last_char_of_lookup_key = word_to_use_for_rule_lookup[-1] if L >=3 else ""
    censored_core_structure = ""

    if L < 2: return original_word_token 
    if L == 2: periods = "."; censored_core_structure = first_char_for_output + periods
    elif L == 3: periods = "."; censored_core_structure = first_char_for_output + periods + last_char_of_lookup_key
    elif L == 4: periods = ".."; censored_core_structure = first_char_for_output + periods + last_char_of_lookup_key
    elif L >= 5: periods = "..."; censored_core_structure = first_char_for_output + periods + last_char_of_lookup_key
    else: return original_word_token
    
    final_censored_core = censored_core_structure
    if derived_is_plural: final_censored_core += "s"
    return prefix + final_censored_core + suffix

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
        if not original_token: processed_words.append(original_token); continue
        is_standalone_hyphen_separator = (original_token == "-")
        processed_word_for_token = ""
        if is_standalone_hyphen_separator: processed_word_for_token = original_token
        elif not is_standalone_hyphen_separator and '-' in original_token: 
            parts = original_token.split('-')
            processed_parts = [ _capitalize_word_part(censor_word_if_needed(p, current_censored_words_set)) for p in parts ]
            processed_word_for_token = '-'.join(processed_parts)
        else: 
            word_after_censorship = censor_word_if_needed(original_token, current_censored_words_set)
            original_token_lower = original_token.lower()
            is_keyword_and_not_censored = (original_token_lower in KEYWORDS and word_after_censorship == original_token)
            if capitalize_next_word_override: processed_word_for_token = _capitalize_word_part(word_after_censorship)
            elif is_keyword_and_not_censored: processed_word_for_token = original_token_lower 
            else: processed_word_for_token = _capitalize_word_part(word_after_censorship)
        processed_words.append(processed_word_for_token)
        if is_standalone_hyphen_separator or original_token.endswith(":"): capitalize_next_word_override = True
        else: capitalize_next_word_override = False
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
    # import gradio as gr # Already imported at the top
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
        ],
        allow_flagging='never'
    )
    return iface

# --- MAIN EXECUTION BLOCK (for standalone running) ---
if __name__ == "__main__":
    print("Title Formatter script running directly. Launching Gradio UI...")
    # The 'gradio' import is at the top of the file.
    # If running locally and Gradio isn't installed, this will fail at import.
    # In Colab, users should !pip install gradio first.
    formatter_app = create_gradio_interface()
    formatter_app.launch(debug=True) # Use share=True if you want a public link when running from Colab
