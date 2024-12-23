from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import os
import pickle


DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.responses.readonly"
]

        
NEW_FORM = {
    "info": {
        "title": "Reservar limpieza",
    }
}

NEW_QUESTIONS = {
    "requests": [
      
        {
            "createItem": {
                "item": {
                    "title": "Su nombre",
                    "questionItem": {
                        "question": {
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    },
                },
                "location": {"index": 0},
            }
        },
    
        {
            "createItem": {
                "item": {
                    "title": "📍 Localidad",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "DROP_DOWN", 
                                "options": [
                                    {"value": "ALTA GRACIA"},
                                    {"value": "DESPEÑADEROS"},
                                    {"value": "ANISACATE"},
                                    {"value": "LA BOLSA"},
                                    {"value": "LOS AROMOS"},
                                    {"value": "FALDA DEL CARMEN"},
                                ],
                            }
                        }
                    },
                },
                "location": {"index": 1},
            }
        },

        {
            "createItem": {
                "item": {
                    "title": "🏡 Dirección",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    },
                },
                "location": {"index": 2},
            }
        },

        {
            "createItem": {
                "item": {
                    "title": "Referencias de la ubicación (opcional)",
                    "questionItem": {
                        "question": {
                            "textQuestion": {}
                        }
                    },
                },
                "location": {"index": 3},
            }
        },
      
        {
            "createItem": {
                "item": {
                    "title": "📱 Ingrese su número de celular",
                    "questionItem": {
                        "question": {
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                    
                },
                "location": {"index": 4},
            }
        },
        {
            "createItem": {
                "item": {
                    "title": "Servicios",
                    "pageBreakItem": {}
                },
                "location": {"index": 5},
            }
        },
    
    # SEGUNDA PAGINA

        {
            "createItem": {
                "item": {
                    "title": "🛠️ Qué tipo de trabajo necesita su pileta?",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO", 
                                "options": [
                                    {"value": "Mantenimiento"},
                                    {"value": "Recuperación del agua"},
                                    {"value": "Vaciado y limpieza total"},
                                    {"value": "Asesoramiento"}
                                ],
                                "shuffle": False,
                            }
                        }
                    },
                },
                "location": {"index": 6},
            }
        },
  
        {
            "createItem": {
                "item": {
                    "title": "📏 Indique las medidas de su pileta (LARGO X ANCHO)",
                    "questionItem": {
                        "question": {
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                    
                },
                "location": {"index": 7},
            }
        },
       
        {
            "createItem": {
                "item": {
                    "title": "Indique día/s de preferencia (opcional)",
                    "questionItem": {
                        "question": {
                            "choiceQuestion": {
                                "type": "CHECKBOX", 
                                "options": [
                                    {"value": "LUNES"},
                                    {"value": "MARTES"},
                                    {"value": "MIERCOLES"},
                                    {"value": "JUEVES"},
                                    {"value": "VIERNES"},
                                    {"value": "SABADO"},
                                ],
                            }
                        }
                    },
                },
                "location": {"index": 8},
            }
        },

        {
            "createItem": {
                "item": {
                    "title": "Horario de preferencia (opcional)",
                    "questionItem": {
                        "question": {
                            "choiceQuestion": {
                                "type": "CHECKBOX", 
                                "options": [
                                    {"value": "MAÑANA"},
                                    {"value": "TARDE"},
                                ],
                            }
                        }
                    },
                },
                "location": {"index": 9},
            }
        },

        {
            "createItem": {
                "item": {
                    "questionItem": {
                        "question": {
                            "choiceQuestion": {
                                "type": "CHECKBOX", 
                                "options": [
                                    {"value": "Marque la casilla si la limpieza es necesitada con urgencia."},
                                ],
                            }
                        }
                    },
                },
                "location": {"index": 10},
            }
        }

    # fin items
    ]
}


def authenticate():
    creds = None

    if os.path.exists("token.json"):
        with open("token.json", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "wb") as token:
            pickle.dump(creds, token)

    return creds


creds = authenticate()

def create_form(creds):
    form_service = build(
                        "forms", 
                        "v1", 
                        credentials=creds, 
                        discoveryServiceUrl=DISCOVERY_DOC
                        )

    # crear formulario
    result = form_service.forms().create(body=NEW_FORM).execute()
    form_id = result.get("formId")

    # agregar preguntas
    form_service.forms().batchUpdate(formId=form_id, body=NEW_QUESTIONS).execute()

    # mostrar enlace
    form_url = result.get("responderUri")
    if form_url:
        print(f"Link del formulario:  {form_url}")
    else:
        print("No se pudo generar el enlace del formulario.")
    
    return result


result = create_form(creds)

form_id = result.get("formId")





