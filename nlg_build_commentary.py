import random
from nlglib.microplanning import *
from nlglib.realisation.simplenlg.realisation import Realiser
realise = Realiser(host='nlg.kutlak.info')

def build_cluases_style1():
    """positive verbs"""
    verbs_p = ["increse", "rise", "surge"]
    chosen_p_verb = random.choice(verbs_p)

    """negative verbs"""
    verbs_n = ["fall", "drop"]
    chosen_n_verb = random.choice(verbs_n)

    adverbs = ["steeply", "sharply"]
    chosen_adverb = random.choice(adverbs)

    return chosen_p_verb,chosen_n_verb, chosen_adverb

def build_commentary_sytle1(account_code, total_variance):
    chosen_p_verb, chosen_n_verb, chosen_adverb = build_cluases_style1()
    if total_variance > 0:
        chosen_verb = chosen_p_verb
    elif total_variance < 0:
        chosen_verb = chosen_n_verb
    subject = NP(account_code)
    verb = VP(chosen_verb)
    verb += Adverb(chosen_adverb)
    report_statement = Clause()
    report_statement.subject = subject
    report_statement.predicate = verb
    report_statement.predicate.complements += PP('by')
    object = NP(total_variance)
    report_statement.object = object
    report_statement['TENSE'] = 'PAST'
    A = (realise(report_statement))
    return A

def build_clauses_substyle1():
    """positive verbs"""
    verbs_p = ["increse in", "rise in", "surge in"]
    chosen_p_verb = random.choice(verbs_p)

    """negative verbs"""
    verbs_n = ["fall in", "drop in", "decrease in"]
    chosen_n_verb = random.choice(verbs_n)

    predicate_verbs = ["attribute", "due"]
    chosen_pred_verbs = random.choice(predicate_verbs)

    return chosen_p_verb, chosen_n_verb, chosen_pred_verbs

def build_commentary_substyle1():
    chosen_p_verb, chosen_n_verb, chosen_pred_verbs = build_cluases_style1()

    reasons1 = Clause()
    reasons1.subject = NP("the variance is")
    reasons1.predicate = VP(chosen_pred_verbs)
    resons1['TeNSe'] = 'PAST'
    reasons1.predicate.complements += PP('to')
    B = realise(reasons1)
    B = B[:-1]
    return  B

def build_commentary_substyle1A(flag, variance_format_rollup):
    chosen_p_verb, chosen_n_verb, chosen_pred_verbs = build_clauses_substyle1()
    parameter = ""
    if flag == "P":
        parameter = chosen_p_verb
    elif flag == "N":
        parameter == chosen_n_verb
    else:
        parameter = ""
    reasons1 = Clause()
    reasons1.subject += NP(parameter)
    reasons1.object = NP(variance_format_rollup)
    B = realise(reasons1)
    B = B[0].lower() + b[1:]
    return B

def build_clauses_style2():
    """positive verbs"""
    verbs_p = ["increse", "rise", "surge"]
    chosen_p_verb = random.choice(verbs_p)

    """negative verbs"""
    verbs_n = ["fall", "drop"]
    chosen_n_verb = random.choice(verbs_n)

    adverbs = ["steep", "sharp"]
    chosen_adverb = random.choice(adverbs)

    return chosen_p_verb, chosen_n_verb, chosen_adverb

def build_commentary_style2(account_code, total_variance):
    chosen_p_verb, chosen_n_verb, chosen_adverb = build_cluases_style2()
    if total_variance > 0:
        chosen_verb = chosen_p_verb
    elif total_variance < 0:
        chosen_verb = chosen_n_verb
    subject = NP(account_code)
    verb = NP(chosen_verb)
    verb += Adverb(chosen_adverb)
    report_statement = Clause()
    report_statement.subject = subject
    report_statement.predicate = verb
    report_statement.predicate.complements += PP('in')
    object = NP(account_code), NP(str("by")), NP(str(total_variance))
    report_statement.predicate.complements += object
    report_statement['TENSE'] = 'PAST'
    A = (realise(report_statement))
    return A

def build_clauses_substyle2():
    """positive verbs"""
    verbs_p = ["increse in", "rise in", "surge in"]
    chosen_p_verb = random.choice(verbs_p)

    """negative verbs"""
    verbs_n = ["fall in", "drop in", "decrease in"]
    chosen_n_verb = random.choice(verbs_n)

    predicate_verbs = ["is attributed", "is due"]
    chosen_pred_verbs = random.choice(predicate_verbs)

    return chosen_p_verb, chosen_n_verb, chosen_pred_verbs

def build_commentary_substyle2():
    chosen_p_verb, chosen_n_verb, chosen_pred_verbs = build_cluases_substyle2()

    reasons1 = Clause()
    reasons1.subject = NP(random.choice([("the reason behind"),("the cause of")]))
    reasons1.subject.complements += NP("variance")
    reasons1.subject.complements += VP(chosen_pred_verbs)
    reasons1['TENSE'] = 'PAST'
    reasons1.subject.complements += PP('to')
    B = realise(reasons1)
    B = B[:-1] + " "
    return B

def build_commendatry_substyle2A(flag, variance_format_rollup):
    chosen_p_verb, chosen_n_verb, chosen_pred_verbs = build_clauses_substyle2()
    parameter = ""
    if flag == "P":
        parameter = chosen_p_verb
    elif flag == "N":
        parameter == chosen_n_verb
    else:
        parameter = ""
    reasons1 = Clause()
    reasons1.subject += NP(parameter)
    reasons1.object = NP(variance_format_rollup)
    B = realise(reasons1)
    B = B[0].lower() + B[1:]
    return B

def build_comments(account_code, flag, total_variance, variance_format_rollup):
    styles = ["1","2"]
    chosen_style = random.choice(styles)
    if chosen_style == "1":
        commentary_main = build_commentary_sytle1(account_code, total_variance)
        commentary_causal1 = build_clauses_substyle1()
        commentary_causal2 = build_commentary_substyle1A(flag, variance_format_rollup)
    else:
        commentary_main = build_commentary_style2(account_code, total_variance)
        commentary_causal1 = build_clauses_substyle2()
        commentary_causal2 = build_commendatry_substyle2A(flag, variance_format_rollup)
    return commentary_main, commentary_causal1, commentary_causal2


if __name__ == '__main__':
    commentary_main, commentary_causal1, commentary_causal2 = build_comments(account_code, flag, total_variance, variance_format_rollup)