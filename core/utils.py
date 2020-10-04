def get_recommendation(data):
    ## Call model function here
    
    SAMPLE_DATA = [	
        {
            "Medication": "Bupropion",
            "Highlights": [
                ["Bupropion is a good follow-up when SSRIs have been unsuccessful.", "https://pubmed.ncbi.nlm.nih.gov24923342/"],
                ["Bupropion is less likely to make you sleepy or induce sexual dysfunction than SSRIs.", "https://pubmed.ncbi.nlm.nih.gov/18370448/"]
            ]
        }, {
            "Medication": "Fluvoxamine",
            "Highlights": [
                ["Fluvoxamine may not be safe if you are breastfeeding.", "https://pubmed.ncbi.nlm.nih.gov/25896469/"],
                ["Fluvoxamine may help with inflammation.", "https://pubmed.ncbi.nlm.nih.gov/30728287/"]
            ]
        }
    ]
    
    return SAMPLE_DATA