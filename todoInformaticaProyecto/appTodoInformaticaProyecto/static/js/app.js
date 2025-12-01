// Espera a que el DOM esté completamente cargado
$(document).ready(function() {
    
    // --- 1. LÓGICA DE AÑADIR AL CARRITO (Página de Producto) ---
    $('#btn-add-to-cart').on('click', function(e) {
        e.preventDefault(); 
        console.log("Click en Añadir al carrito");

        const productId = $(this).data('product-id');
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        
        const $button = $(this);
        const originalText = $button.html();
        
        $button.prop('disabled', true).text('Añadiendo...');

        $.ajax({
            url: '/api/add-to-cart/', 
            type: 'POST',
            data: {
                'product_id': productId,
                'csrfmiddlewaretoken': csrfToken
            },
            dataType: 'json', 
            success: function(response) {
                const $successMsg = $('#success-message');
                $successMsg.text(`¡Añadido! Total: ${response.cart_count}`)
                           .fadeIn(400).delay(2000).fadeOut(400, function() {
                                $button.prop('disabled', false).html(originalText);
                           });
                // Actualizar contador del menú si existe
                $('#nav-cart-count').text(response.cart_count);
            },
            error: function(xhr, status, error) {
                console.error("Error al añadir:", error);
                alert("Error al conectar con el servidor.");
                $button.prop('disabled', false).html(originalText);
            }
        });
    });

    // --- 2. LÓGICA DE ACTUALIZAR CANTIDAD (+ y -) ---
    // Usamos $(document).on para que funcione aunque los elementos cambien
    $(document).on('click', '.btn-update-cart', function(e) {
        e.preventDefault();
        
        const productId = $(this).data('product-id');
        const action = $(this).data('action');
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        console.log(`Actualizando: ID ${productId}, Acción: ${action}`);

        $.ajax({
            url: '/api/update-cart-item/',
            type: 'POST',
            data: {
                'product_id': productId,
                'action': action,
                'csrfmiddlewaretoken': csrfToken
            },
            dataType: 'json',
            success: function(response) {
                if (response.status === 'success') {
                    // Recargamos la página para ver los precios actualizados
                    location.reload(); 
                } else {
                    alert("Error: " + response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error al actualizar:", xhr.responseText);
                alert("Hubo un error al actualizar el carrito.");
            }
        });
    });

    // --- 3. LÓGICA DE ELIMINAR PRODUCTO (Papelera) ---
    $(document).on('click', '.btn-remove-item', function(e) {
        e.preventDefault();
        
        if(!confirm("¿Seguro que quieres eliminar este producto?")) return;

        const productId = $(this).data('product-id');
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        console.log(`Eliminando: ID ${productId}`);

        $.ajax({
            url: '/api/remove-from-cart/',
            type: 'POST',
            data: {
                'product_id': productId,
                'csrfmiddlewaretoken': csrfToken
            },
            dataType: 'json',
            success: function(response) {
                if (response.status === 'success') {
                    location.reload();
                } else {
                    alert("Error: " + response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error al eliminar:", xhr.responseText);
                alert("Hubo un error al eliminar el producto.");
            }
        });
    });

});