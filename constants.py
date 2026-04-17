#Data that's never be changed
TEACHERS = [
    "Lock",
    "Glen",
    "Banks",
    "Richards",
    "Shaw",
    "Singer",
    "Uther",
    "Tyler",
    "Numen",
    "Zelden"
]

CLASSROOMS = [
    "Beach 201",
    "Beach 301",
    "Frank 119",
    "Loft 206",
    "Loft 310",
    "James 325",
    "Roman 201",
    "Roman 216",
    "Slater 003",
]

ROOM_CAPACITY = {
    "Beach 201": 18,
    "Beach 301": 25,
    "Frank 119": 95,
    "Loft 206": 55,
    "Loft 310": 48,
    "James 325": 110,
    "Roman 201": 40,
    "Roman 216": 80,
    "Slater 003": 32
}

TIMES = [
    "10 AM",
    "11 AM", 
    "12 PM",    
    "1 PM",    
    "2 PM",    
    "3 PM"    
]

#Sections
SECTIONS = [
    "SLA101A",
    "SLA101B",
    "SLA191A",
    "SLA191B",
    "SLA201",
    "SLA291",
    "SLA303",
    "SLA304",
    "SLA394",
    "SLA499",
    "SLA451",
]

EXPECTED_STUDENTS = {
    "SLA101A": 40,
    "SLA101B": 35,
    "SLA191A": 45,
    "SLA191B": 40,
    "SLA201": 60,
    "SLA291": 50,
    "SLA303": 25,
    "SLA304": 20,
    "SLA394": 15,
    "SLA499": 30,
    "SLA451": 90
}

#Other data
PREFERRED_CLASSES = {
    "SLA101A": {"Glen", "Lock", "Banks"},
    "SLA101B": {"Glen", "Lock", "Banks"},

    "SLA191A": {"Glen", "Lock", "Banks"},
    "SLA191B": {"Glen", "Lock", "Banks"},

    "SLA201":  {"Glen", "Banks", "Zeldin", "Lock", "Singer"},
    "SLA291":  {"Glen", "Banks", "Zeldin", "Lock", "Singer"},

    "SLA303":  {"Glen", "Zeldin"},
    "SLA304":  {"Singer", "Uther"},

    "SLA394":  {"Tyler", "Singer"},

    "SLA449":  {"Tyler", "Zeldin", "Uther"},

    "SLA451":  {"Lock", "Banks", "Zeldin"},
}

SLIGHT_PREFERRED_CLASSES = {
    "SLA101A": {"Numen", "Richards", "Shaw", "Singer"},
    "SLA101B": {"Numen", "Richards", "Shaw", "Singer"},

    "SLA191A": {"Numen", "Richards", "Shaw", "Singer"},
    "SLA191B": {"Numen", "Richards", "Shaw", "Singer"},

    "SLA201":  {"Richards", "Uther", "Shaw"},
    "SLA291":  {"Richards", "Uther", "Shaw"},

    "SLA303":  {"Banks"},
    "SLA304":  {"Richards"},

    "SLA394":  {"Richards", "Zeldin"},

    "SLA449":  {"Zeldin", "Shaw"},   # Zeldin appears in both lists; still valid

    "SLA451":  {"Tyler", "Singer", "Shaw", "Glen"},
}


