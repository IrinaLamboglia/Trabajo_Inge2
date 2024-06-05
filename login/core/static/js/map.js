var map = L.map('map').setView([-34.9214, -57.9544], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


// Función para listar filiales
function listarFiliales() {
  fetch('/listar_filiales/')
      .then(response => response.json())
      .then(data => {
          data.forEach(filial => {
              var popupContent = `<b>${filial.nombre}</b><br>`;
              popupContent += filial.ayudante ? `Ayudante: ${filial.ayudante}` : 'La filial aun no tiene ayudante';
              
              var marker = L.marker([filial.latitud, filial.longitud]).addTo(map)
                .bindPopup(popupContent)
                .openPopup();
          });
      })
      .catch(error => {
          console.error('Error al listar filiales:', error);
      });
}

// Llamar a la función listarFiliales cuando se carga la página
document.addEventListener('DOMContentLoaded', listarFiliales);



var agregarFilial = false;

// Event listener para el botón "Agregar Filial"
  document.getElementById('agregar-filial-btn').addEventListener('click', function() {
    agregarFilial = true; 

    this.disabled = true; 
    

    map.on('click', function(e) {
        if (agregarFilial) {
            var latitud = e.latlng.lat;
            var longitud = e.latlng.lng;
            

   
            var marker = L.marker([latitud, longitud]).addTo(map);

           
            var nombreFilial = prompt("Ingrese el nombre de la nueva filial:");

            marker.bindPopup(nombreFilial)
            .openPopup();

            if (nombreFilial !== null && nombreFilial.trim() !== '') {
                
                  fetch('/guardar_filial/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') 
                    },
                    body: JSON.stringify({
                        nombre: nombreFilial,
                        latitud: latitud,
                        longitud: longitud
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message); 
                })
                .catch(error => {
                    console.error('Error:', error);
                });

                window.location.reload();


            } else {
                map.removeLayer(marker);
            }

            agregarFilial = false;
    
            document.getElementById('agregar-filial-btn').disabled = false;
        }
    });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
function eliminarFilial(filialId) {
    if (confirm("¿Estás seguro de que quieres eliminar esta filial?")) {
      fetch(`/eliminar_filial/${filialId}/`, {
        method: 'POST', // Cambiar a POST
        headers: {
          'X-CSRFToken': getCookie('csrftoken')
        },
      })
        .then(response => {
            if (response.ok) {
                alert("Filial eliminada correctamente");
                window.location.reload();
            } else {
                alert("No se puede eliminar la filial porque tiene un ayudante asignado.");
            }
        })
        .catch(error => console.error('Error al eliminar la filial:', error));
    }
}