const { createApp } = Vue

createApp({
  data() {
    return {
      nuevoContacto: {
        nombre: '',
        email: '',
        telefono: ''
      },
      contactos: [
        { nombre: 'David Trueba', email: 'Davidllueva@gmail.com', telefono: '123456789' },
        { nombre: 'Gonzalo Iglesias ', email: 'Gonzaloiglesias@gmail.com', telefono: '987654321' },
        { nombre: 'Alex Iñurgaitz ', email: 'Alexiturgaitz@gmail.com', telefono: '987654321' }
    
      ]
    }
  },
  methods: {
    agregarContacto() {
      if(this.nuevoContacto.nombre && this.nuevoContacto.email) {
        this.contactos.push({ ...this.nuevoContacto });
        this.nuevoContacto = { nombre: '', email: '', telefono: '' };
      } else {
        alert("Por favor completa nombre y email");
      }
    },
    borrarContacto(index) {
      this.contactos.splice(index, 1);
    },
   
  },
  mounted() {
    const datosGuardados = localStorage.getItem('agenda-vue');
    if (datosGuardados) {
      this.contactos = JSON.parse(datosGuardados);
    }
  }
}).mount('#app')