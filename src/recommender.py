def get_recommend_genre(age):
    
    if age<18:
        recommend_genre="upbeat, trending, clean content"
    elif age>=18 and age<=30:
        recommend_genre="pop, EDM, hip-hop, indie"
    elif age>=30 and age<=45:
        recommend_genre="classics, soft rock, melodic"
    else:
        recommend_genre="old classics, devotional, calm music"

    return recommend_genre