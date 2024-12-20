# helpers.py

# Zmienna globalna do zarządzania statusem slajdów
direct_slides_viewed = False
coherent_slides_viewed = False

def mark_direct_slides_as_viewed():
    global direct_slides_viewed
    direct_slides_viewed = True

def mark_coherent_slides_as_viewed():
    global coherent_slides_viewed
    coherent_slides_viewed = True

def are_all_slides_viewed():
    return direct_slides_viewed and coherent_slides_viewed
