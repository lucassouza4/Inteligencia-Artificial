def abduction(knowledge_base, observation):
    explanation = []
    obs_rules = []
    consequences = []
    
    run = True

    if 'assumables' in knowledge_base:
        for assumable in knowledge_base['assumables']:
            if not assumable in consequences:
                consequences.append(assumable)

    while run:
        run = False

        for i in knowledge_base['rules']:
            if i not in consequences:
                for j in knowledge_base['rules'][i]:
                    if not set(j).difference(set(consequences)):
                        consequences.append(i)
                        run = True

    for obs in observation:
        obs_rules += knowledge_base["rules"][obs]

    for res in obs_rules:
        is_explanation =  test_consequence_assumables(res, consequences, knowledge_base)
        
        if is_explanation and not (res in explanation):
            explanation += [res]

    return explanation


def test_consequence_assumables(r, consequences, kb):
    is_explanation = True

    for a in r:
        if not (a in consequences or a in kb["assumables"]):
            is_explanation = False
            break

    return is_explanation


if __name__ == "__main__":
    knowledge_base = [
                        {
                            'rules':{
                                'bronquite': [['influenza'], ['fuma']],
                                'tosse': [['bronquite']],
                                'chiado': [['bronquite']],
                                'febre': [['influenza', 'infecção']],
                                'dor de garganta': [['influenza']]
                            },
                            'assumables': ['fuma', 'não fumante', 'influenza', 'infecção']
                        },
                        {
                            'rules':{
                                'alarme': [['invasão'], ['fogo']],
                                'fumaça': [['fogo']],
                            },
                            'assumables': ['fogo', 'invasão']
                        }
                    ]
    observation = [
                    ['chiado', 'febre', 'dor de garganta'],
                    ['tosse', 'febre'],
                    ['alarme']
                ]
    
    print(f"observations: {observation[0]} ===> explanations obtained: {abduction(knowledge_base[0], observation[0])}")

    print(f"observations: {observation[1]} ===> explanations obtained: {abduction(knowledge_base[0], observation[1])}")

    print(f"observations: {observation[2]} ===> explanations obtained: {abduction(knowledge_base[1], observation[2])}")
