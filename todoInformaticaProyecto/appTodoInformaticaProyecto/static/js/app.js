// Espera a que el DOM este cargado entero funcion jquery
$(document).ready(function() {
    
    // Captura  click en el boton añadir al carrito
    $('#btn-add-to-cart').on('click', function(e) {
        e.preventDefault(); 

        const productId = $(this).data('product-id');
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        
        const $button = $(this);
        const originalText = $button.html();
        
        // Deshabilitar boton cuando sea clickado
        $button.prop('disabled', true).text('Añadiendo...');

        // ajax
        $.ajax({
            url: '/api/add-to-cart/', // La URL en urls.py
            type: 'POST',
            data: {
                'product_id': productId,
                'csrfmiddlewaretoken': csrfToken
            },
            dataType: 'json', 
            
            success: function(response) {
                // manipular dom
                const $successMsg = $('#success-message');
                
                $successMsg.text(`¡Producto añadido! Total en carrito: ${response.cart_count} items.`)
                           .fadeIn(400) // mostrar suave
                           .delay(2000) // Esperar 2 segundos
                           .fadeOut(400, function() { // ocultar suave
                                // Restaurar el boton al terminar
                                $button.prop('disabled', false).html(originalText);
                           });
            },
            
            error: function(xhr, status, error) {
                console.error("Error al añadir al carrito:", status, error);
                alert("Hubo un error al contactar al servidor. Inténtalo de nuevo.");
                $button.prop('disabled', false).html(originalText);
            }
        });
    });
});