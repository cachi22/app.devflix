var persona = {
    nombre: 'Juan',
    edad: 30,
    ciudad: "madrid",
    saludar : function () {
        console.log("Hola soy " + this.nombre);
    }
};

console.log(persona.nombre);
persona.saludar();


