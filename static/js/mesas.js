let pedidos = {}; 
const formatter = new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0
});


mesaCount = 0
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript cargado correctamente.');
});

function addMesa() {
    mesaCount++;
    const mesaList = document.getElementById('mesaList');
    const newMesa = document.createElement('div');
    newMesa.className = 'col-md-4';
    newMesa.id = `mesa-${mesaCount}`;
    let opciones = '';
    productos.forEach(producto => {
        opciones += `<option value="${producto.fields.nombre}">${producto.fields.nombre}</option>`;
    });

    let toppingOptions = '';
    toppings.forEach(topping => {
        console.log(topping.fields);
        precio_topping = parseInt(topping.fields.precio);
        toppingOptions += `<div>
            <input type="checkbox" id="topping-${mesaCount}-${topping.fields.nombre}" value="${topping.fields.nombre}" data-precio="${precio_topping}">
            <label for="topping-${mesaCount}-${topping.fields.nombre}">${topping.fields.nombre} (+${formatter.format(precio_topping)})</label>
        </div>`;
    });

    newMesa.innerHTML = `
        <div class="card mb-4 mesa-card">
            <div class="card-body">
                <h5 class="card-title">Mesa ${mesaCount}</h5>
                <select class="form-select mb-3" id="producto-${mesaCount}">
                    ${opciones}
                </select>
                <div class="quantity-controls">
                    <button class="btn btn-secondary quantity-btn" onclick="changeQuantity(${mesaCount}, -1)">-</button>
                    <input type="number" id="quantity-${mesaCount}" value="1" min="1" class="form-control quantity-input">
                    <button class="btn btn-secondary quantity-btn" onclick="changeQuantity(${mesaCount}, 1)">+</button>
                </div>
                <div class="toppings-section">
                    <h6>Toppings</h6>
                    ${toppingOptions}
                </div>
                <button class="btn btn-success" onclick="addPedido(${mesaCount})">Agregar Pedido</button>
                <button class="btn btn-info" onclick="showPedidos(${mesaCount})">Ver Pedido</button>
                <button class="btn btn-warning" onclick="pagarCuenta(${mesaCount})">Pagar Cuenta</button>
            </div>
        </div>
    `;
    mesaList.appendChild(newMesa);
    pedidos[mesaCount] = []; // Inicializa el array de pedidos para la nueva mesa
}

function changeQuantity(mesaId, delta) {
    const quantityInput = document.getElementById(`quantity-${mesaId}`);
    let quantity = parseInt(quantityInput.value);
    quantity = Math.max(1, quantity + delta); // Asegura que la cantidad no sea menor que 1
    quantityInput.value = quantity;
}

function addPedido(mesaId) {

    const productoSelect = document.getElementById(`producto-${mesaId}`);
    const producto = productoSelect.value;
    const quantityInput = document.getElementById(`quantity-${mesaId}`);
    const quantity = parseInt(quantityInput.value);
    let precio_base = 0;
    productos.forEach(product => {
        if (product.fields.nombre === producto) {
            precio_base = quantity * product.fields.precio_base;
        }
    });

    const selectedToppings = [];
    let toppingCost = 0;
    toppings.forEach(topping => {
        const toppingCheckbox = document.getElementById(`topping-${mesaId}-${topping.fields.nombre}`);
        if (toppingCheckbox.checked) {
            selectedToppings.push(topping.fields.nombre);
            toppingCost += topping.fields.precio * quantity;
            
        }
    });
    const totalPrecio = precio_base + toppingCost;

    if (!pedidos[mesaId]) {
        pedidos[mesaId] = [];
    }
    pedidos[mesaId].push({ producto, quantity, precio_base: totalPrecio, toppings: selectedToppings });
    alert(`Producto ${producto} (Cantidad: ${quantity}) con toppings ${selectedToppings.join(', ')} agregado a la mesa ${mesaId}`);
}

function showPedidos(mesaId) {
    const pedidoList = pedidos[mesaId] || [];
    showPopup(`Pedidos de la mesa ${mesaId}`, pedidoList, mesaId);
}

function pagarCuenta(mesaId) {
    const pedidoList = pedidos[mesaId] || [];
    const total = pedidoList.reduce((sum, pedido) => sum + pedido.quantity, 0); // Calcula el total (puedes ajustar esto según los precios)
    registrarPago(mesaId, total, pedidoList);
    showPopup(`Total a pagar para la mesa ${mesaId}`, pedidoList, mesaId);
    //pedidos[mesaId] = []; // Reinicia los pedidos de la mesa
}

function registrarPago(mesaId, total, pedidoList) {
    fetch(registrarPagoUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ mesa_id: mesaId, total: total, pedidos: pedidoList })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log(`Pago registrado para la mesa ${mesaId}: ${total} items`);
        } else {
            console.error('Error al registrar el pago');
        }
    })
    .catch(error => console.error('Error:', error));
}

function showPopup(title, pedidoList, mesaId) {
    document.getElementById('popup-title').textContent = title;
    const popupBody = document.getElementById('popup-body');
    popupBody.innerHTML = ''; // Clear previous content

    if (pedidoList.length > 0) {
        const table = document.createElement('table');
        table.className = 'table table-striped';
        const thead = document.createElement('thead');
        thead.innerHTML = `<tr>
                    <th>Producto</th>
                    <th>Cantidad</th>
                    <th>Precio</th>
                    <th>Toppings</th>
                    <th>Acciones</th>
                </tr>`;
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        let suma = 0;
        
        pedidoList.forEach((p, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${p.producto}</td>
                <td>${p.quantity}</td>
                <td>${formatter.format(p.precio_base)}</td>
                <td>${p.toppings.join(', ')}</td>
                <td><button class="btn btn-danger" onclick="deletePedido(${mesaId}, ${index})">Eliminar</button></td>`;
            suma += p.precio_base;
            tbody.appendChild(row);
        });
        const totalRow = document.createElement('tr');
        totalRow.innerHTML = `
                <td colspan="3"><strong>Total</strong></td>
                <td><strong>${formatter.format(suma)}</strong></td>
                <td></td>`;
        tbody.appendChild(totalRow);
        table.appendChild(tbody);
        popupBody.appendChild(table);
    } else {
        popupBody.textContent = 'No hay pedidos.';
    }

    document.getElementById('popup').style.display = 'block';
}

function deletePedido(mesaId, index) {
    pedidos[mesaId].splice(index, 1);
    showPedidos(mesaId); // Actualiza el popup después de eliminar el pedido
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}  