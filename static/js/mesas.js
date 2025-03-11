// Inicializa el contador con el número de mesas existentes
let pedidos = {}; // Objeto para almacenar los pedidos de cada mesa

document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript cargado correctamente.');
});

function addMesa() {
    mesaCount++;
    const mesaList = document.getElementById('mesaList');
    const newMesa = document.createElement('div');
    newMesa.className = 'col-md-4';
    newMesa.id = `mesa-${mesaCount}`;
    newMesa.innerHTML = `
        <div class="card mb-4 mesa-card">
            <div class="card-body">
                <h5 class="card-title">Mesa ${mesaCount}</h5>
                <select class="form-select mb-3" id="producto-${mesaCount}">
                    <option value="Aguila">Aguila</option>
                    <option value="Poker">Poker</option>
                    <option value="Club Colombia">Club Colombia</option>
                </select>
                <div class="quantity-controls">
                    <button class="btn btn-secondary quantity-btn" onclick="changeQuantity(${mesaCount}, -1)">-</button>
                    <input type="number" id="quantity-${mesaCount}" value="1" min="1" class="form-control quantity-input">
                    <button class="btn btn-secondary quantity-btn" onclick="changeQuantity(${mesaCount}, 1)">+</button>
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
    if (!pedidos[mesaId]) {
        pedidos[mesaId] = [];
    }
    pedidos[mesaId].push({ producto, quantity });
    alert(`Producto ${producto} (Cantidad: ${quantity}) agregado a la mesa ${mesaId}`);
}

function showPedidos(mesaId) {
    const pedidoList = pedidos[mesaId] || [];
    showPopup(`Pedidos de la mesa ${mesaId}`, pedidoList, mesaId);
}

function pagarCuenta(mesaId) {
    const pedidoList = pedidos[mesaId] || [];
    const total = pedidoList.reduce((sum, pedido) => sum + pedido.quantity, 0); // Calcula el total (puedes ajustar esto según los precios)
    registrarPago(mesaId, total);
    showPopup(`Total a pagar para la mesa ${mesaId}`, pedidoList, mesaId);
    pedidos[mesaId] = []; // Reinicia los pedidos de la mesa
}

function registrarPago(mesaId, total) {
    fetch(registrarPagoUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ mesa_id: mesaId, total: total })
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
        thead.innerHTML = '<tr><th>Producto</th><th>Cantidad</th><th>Acciones</th></tr>';
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        pedidoList.forEach((p, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${p.producto}</td><td>${p.quantity}</td><td><button class="btn btn-danger" onclick="deletePedido(${mesaId}, ${index})">Eliminar</button></td>`;
            tbody.appendChild(row);
        });
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