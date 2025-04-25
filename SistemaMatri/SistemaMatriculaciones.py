import json

class PlanEstudio():
    """
    Clase encargada de gestionar la carga del plan de estudio desde un archivo JSON.
    """

    def __init__(self, archivo="PlanEstudio2021.json"):
        """
        Inicializa la clase con el nombre del archivo del plan de estudio.

        Args:
            archivo (str): Ruta del archivo JSON que contiene el plan de estudio.
        """
        self.archivo = archivo

    def cargarPlanEstudio(self):
        """
        Carga el contenido del archivo JSON del plan de estudio.

        Returns:
            dict: Contenido completo del plan de estudio.
        """
        with open(self.archivo, "r", encoding="utf-8") as archivoPlan:
            self.plan2021 = json.load(archivoPlan)
        return self.plan2021


class UC():
    """
    Representa una unidad curricular (materia) del plan de estudio.
    """

    def __init__(self, plan: PlanEstudio, semestre: str, codigo: str):
        """
        Inicializa una UC especificando el plan, semestre y código.

        Args:
            plan (PlanEstudio): Objeto con el plan cargado.
            semestre (str): Clave del semestre correspondiente en el diccionario.
            codigo (str): Código de la unidad curricular.
        """
        self.plan = plan.cargarPlanEstudio()
        self.semestre = semestre
        self.codigo = codigo

    def infoUC(self):
        """
        Extrae la información asociada a la UC (nombre, previas y créditos).

        Returns:
            True: Los datos se obtienen correctamente.
            False: Las credenciales ingresadas son incorrectas
        """
        try:
            info = self.plan[self.semestre][self.codigo]
            materia = info["Nombre"]
            previas = info["Previas"]
            creditos = info["Creditos"]
            self.infoMateria = (materia, previas, creditos)
            return True
        except:
            self.infoMateria = None
            raise KeyError ("La credenciales ingresadas son incorrectas")
        
    def nombreMateria(self):
        """
        Devuelve el nombre de la materia.

        Returns:
            str: Nombre de la materia.
        """
        if self.infoMateria == None:
            raise TypeError("...")
        return self.infoMateria[0]

    def nombrePrevias(self):
        """
        Devuelve la lista de materias previas de la unidad curricular.

        Returns:
            list: Lista de materias previas.
        """
        if self.infoMateria == None:
            raise TypeError("Error: Códigos Incorrectos")
        return self.infoMateria[1]

    def getCreditos(self):
        """
        Devuelve la cantidad de créditos de la materia.

        Returns:
            int: Créditos de la materia.
        """
        if self.infoMateria == None:
            raise TypeError("...")
        return self.infoMateria[2]


class GestorExpediente:
    """
    Crea, carga y modifica archivos JSON para cada estudiante.
    Permite almacenar y gestionar sus datos.
    """

    def __init__(self, nombre: str, ci: int, añoIngreso: int):
        """
        Inicializa la clase con los datos del estudiante.

        Args:
            nombre (str): Nombre del estudiante.
            ci (int): Cédula de identidad del estudiante.
            añoIngreso (int): Año de ingreso a la carrera.
        """
        self.datos = {"Nombre": nombre,
                      "Cedula": ci,
                      "Año Ingreso": añoIngreso,
                      "Materias Aprobadas": [],
                      "Materias Matriculadas": [],
                      "Inscripción Examen": [],
                      "Créditos": 0}

        nombre_archivo = nombre.replace(" ", "_")
        self.archivo = f"{nombre_archivo}_{ci}.json"

    def crearArchivo(self, indentacion: int = 4):
        """
        Crea un archivo JSON para el estudiante con datos iniciales.

        Args:
            indentacion (int): Nivel de indentación para el formato JSON.
        """
        with open(self.archivo, 'w', encoding='utf-8') as file:
            json.dump(self.datos, file, ensure_ascii=False, indent=indentacion)

        self.data = self.datos

    def cargarDatos(self):
        """
        Carga el contenido del archivo JSON del estudiante.

        Returns:
            dict: Datos del estudiante.
        """
        with open(self.archivo, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        return self.data

    def agregarExamenInscripto(self, uc: UC):
        """
        Agrega una UC a la lista de "Inscripción Examen".

        Args:
            uc (UC): Objeto UC de la materia que se quiere agregar.

        Returns:
            bool: True si se inscribió correctamente, False si ya estaba inscrita.
        """
        datos = self.cargarDatos()
        nombre_uc = uc.nombreMateria()

        if nombre_uc not in datos["Inscripción Examen"]:
            datos["Inscripción Examen"].append(nombre_uc)
        else:
            return False

        with open(self.archivo, 'w', encoding='utf-8') as file:
            json.dump(datos, file, ensure_ascii=False, indent=4)

        self.data = datos
        return True

    def quitarUcExamen(self, materia: UC):
        """
        Elimina una UC de la lista de inscripción a examen.

        Args:
            materia (UC): Objeto UC de la materia a eliminar.
        """
        datos = self.cargarDatos()
        uc = materia.nombreMateria()

        if uc in datos["Inscripción Examen"]:
            datos["Inscripción Examen"].remove(uc)

        with open(self.archivo, 'w', encoding='utf-8') as file:
            json.dump(datos, file, ensure_ascii=False, indent=4)

        self.data = datos

    def agregarUcsAprobadas(self, materia: UC):
        """
        Agrega una UC aprobada y suma sus créditos.

        Args:
            materia (UC): Objeto UC de la materia a agregar.

        Returns:
            bool: True si la materia se agregó correctamente.
        """
        datos = self.cargarDatos()
        uc = materia.nombreMateria()
        creditos = materia.getCreditos()

        if uc not in datos["Materias Aprobadas"]:
            datos["Materias Aprobadas"].append(uc)
            datos["Créditos"] += creditos

        with open(self.archivo, 'w', encoding='utf-8') as file:
            json.dump(datos, file, ensure_ascii=False, indent=4)

        self.data = datos
        return True

    def quitarUcsAprobadas(self, materia: UC):
        """
        Elimina una UC aprobada y descuenta sus créditos.

        Args:
            materia (UC): Objeto UC de la materia a eliminar.
        """
        datos = self.cargarDatos()
        uc = materia.nombreMateria()
        creditos = materia.getCreditos()

        if uc in datos["Materias Aprobadas"]:
            datos["Materias Aprobadas"].remove(uc)
            datos["Créditos"] -= creditos

        with open(self.archivo, 'w', encoding='utf-8') as file:
            json.dump(datos, file, ensure_ascii=False, indent=4)

        self.data = datos

    def inscriptos(self, materia2: UC):

        archivo = "Registros.json"
        uc = materia2.nombreMateria()
        nombre = self.data['Nombre']

        with open(archivo, 'r', encoding='utf-8') as file2:
            self.contenido = json.load(file2)

        if uc not in self.contenido:
            self.contenido[uc] = []
        
        if nombre not in self.contenido[uc]:
            self.contenido[uc].append(nombre)

        with open(archivo, 'w', encoding='utf-8') as file3:
            json.dump(self.contenido, file3, ensure_ascii=False, indent=4)

    def matricular(self, materia: UC):

        datos = self.cargarDatos()
        uc = materia.nombreMateria()

        if uc not in datos["Materias Matriculadas"]:
            datos["Materias Matriculadas"].append(uc)

        with open(self.archivo, 'w', encoding='utf-8') as file:
            json.dump(datos, file, ensure_ascii=False, indent=4)

        self.data = datos

        self.inscriptos(materia)

    def desmatricular(self, materia: UC):

        datos = self.cargarDatos()
        uc = materia.nombreMateria()
        creditos = materia.getCreditos()

        if uc in datos["Materias Matriculadas"]:
            datos["Materias Matriculadas"].remove(uc)

        with open(self.archivo, 'w', encoding='utf-8') as file:
            json.dump(datos, file, ensure_ascii=False, indent=4)

        self.data = datos

    def verListaInscriptos(self, registro = "Registros.json"):
        self.registros = registro
        with open(self.registros, "r", encoding="utf-8") as ver_registros:
            ver_registros = json.load(ver_registros)
        return ver_registros


class Estudiante():
    """
    Representa un estudiante y permite consultar sus datos académicos.
    """

    def __init__(self, usuario: GestorExpediente):
        """
        Inicializa el estudiante a partir de un archivo gestionado por GestorExpediente.

        Args:
            usuario (GestorExpediente): Gestor del archivo JSON del estudiante.
        """
        self.usuario = usuario

        self.datosEstudiante = usuario.cargarDatos()
        self.nombre = self.datosEstudiante["Nombre"]
        self.cedula = self.datosEstudiante["Cedula"]
        self.aprobadas = self.datosEstudiante["Materias Aprobadas"]
        self.matriculadas = self.datosEstudiante["Materias Matriculadas"]
        self.examen = self.datosEstudiante["Inscripción Examen"]
        self.creditos = self.datosEstudiante["Créditos"]

    def infoEstudiante(self):
        """
        Devuelve nombre y cédula del estudiante.

        Returns:
            tuple: Nombre y cédula del estudiante.
        """
        return self.nombre, self.cedula

    def ucsAprobadas(self):
        """
        Retorna una lista con las materias aprobadas del estudiante.

        Returns:
            list: Materias aprobadas.
        """
        return self.aprobadas

    def inscribirseExamen(self, materia: UC):
        """
        Permite al estudiante inscribirse a un examen si cumple con las previas.

        Args:
            materia (UC): Objeto UC con la información de la materia.

        Returns:
            bool: True si cumple con las previas, False si no cumple.
        """
        requisitos = materia.nombrePrevias()
        uc = materia.nombreMateria()

        if not requisitos:
            self.usuario.agregarExamenInscripto(materia)
            return True

        for requisito in requisitos:
            if requisito not in self.aprobadas and requisito not in self.matriculadas:
                return False

        self.usuario.agregarExamenInscripto(materia)
        return True

    def quitatExamen(self, materia: UC):
        """
        Método para eliminar la inscripción a un examen.

        Args:
            materia (UC): Materia a quitar.
        """
        self.usuario.quitarUcExamen(materia)
    
    def matricularUC(self, materia: UC):
        previas = materia.nombrePrevias()

        if not previas:
            self.usuario.matricular(materia)
            return True

        for previa in previas:
            if previa not in self.aprobadas and previa not in self.examen and previa not in self.matriculadas:
                return False

        self.usuario.matricular(materia)
        return True
    
    def desmatricularUC(self, materia: UC):
        self.usuario.desmatricular(materia)

    def __str__(self):
        """
        Representación en string del estudiante.

        Returns:
            str: Información básica del estudiante.
        """
        return (f"Información del estudiante:\n"
                f"Nombre: {self.nombre}\n"
                f"C.I: {self.cedula}\n"
                f"Materias aprobadas: {self.aprobadas}\n"
                f"Materias Matriculadas: {self.matriculadas}\n"
                f"Inscripcion Examenes: {self.examen}\n"
                f"Créditos: {self.creditos}")


class Secretaria():
    """ 
    Representa a la coordinadora o secretaria académica.
    """

    def __init__(self, nombre: str):
        """
        Inicializa la secretaria.

        Args:
            nombre (str): Nombre de la secretaria.
        """
        self.nombre = nombre

    def cargarEstudiante(self, expediente: GestorExpediente):
        """
        Carga un estudiante desde su expediente.

        Args:
            expediente (GestorExpediente): Archivo del estudiante.
        """
        self.expediente = expediente
        self.estudiante = Estudiante(expediente)

    def inscribirEstExamen(self, materia: UC):
        """
        Inscribe al estudiante a un examen.

        Args:
            materia (UC): Objeto UC al que se quiere inscribir.
        """
        self.estudiante.inscribirseExamen(materia)

    def quitarExamenEstudiante(self, materia: UC):
        """
        Elimina una inscripción a examen.

        Args:
            materia (UC): Materia a quitar.
        """
        self.estudiante.quitatExamen(materia)

    def agregar_uc_aprobada(self, aprobada: UC) -> bool:
        """
        Agrega una materia aprobada al expediente del estudiante.

        Args:
            aprobada (UC): Objeto UC de la materia a agregar.

        Returns:
            bool: True si se agregó correctamente, False si ya existía.
        """
        uc = aprobada.nombreMateria()
        if uc not in self.estudiante.ucsAprobadas():
            self.expediente.agregarUcsAprobadas(aprobada)
            return True
        return False

    def quitar_uc(self, materia: UC) -> bool:
        """
        Elimina una UC aprobada del expediente.

        Args:
            materia (UC): Objeto UC de la materia a eliminar.

        Returns:
            bool: True si se eliminó correctamente.
        """
        self.expediente.quitarUcsAprobadas(materia)
        return True
    
    def matricularEstudiante(self, materia: UC):
        self.estudiante.matricularUC(materia)

    def desmatricularEstudiante(self, materia: UC):
        self.estudiante.desmatricularUC(materia)
    
    def verInscriptos(self):
        return self.expediente.verListaInscriptos()