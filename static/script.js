// ============ SISTEMA DE NOTIFICACIONES ============

function mostrarNotificacion(mensaje, tipo = 'info') {
    // tipo puede ser: 'success', 'error', 'warning', 'info'
    const colores = {
        success: 'linear-gradient(to right, #00b09b, #96c93d)',
        error: 'linear-gradient(to right, #ff5f6d, #ffc371)',
        warning: 'linear-gradient(to right, #f2994a, #f2c94c)',
        info: 'linear-gradient(to right, #667eea, #764ba2)'
    };

    Toastify({
        text: mensaje,
        duration: 3000,  // 3 segundos
        gravity: "top",  // top o bottom
        position: "center", // left, center o right
        stopOnFocus: true,
        style: {
            background: colores[tipo] || colores.info,
            borderRadius: "8px",
            fontSize: "14px",
            fontWeight: "500"
        }
    }).showToast();
}

// ============ AUTENTICACIÓN ============

function obtenerToken() {
    return localStorage.getItem('token');
}

function obtenerUsuario() {
    const usuario = localStorage.getItem('usuario');
    return usuario ? JSON.parse(usuario) : null;
}

function getAuthHeaders() {
    const token = obtenerToken();
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

function cerrarSesion() {
    if (confirm('¿Seguro que quieres cerrar sesión?')) {
        localStorage.removeItem('token');
        localStorage.removeItem('usuario');
        sessionStorage.removeItem('session_active');
        window.location.href = '/static/login.html';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("FinanzasPro Web cargada correctamente.");

    // 1. Verificar si hay token base
    const token = obtenerToken();
    if (!token) {
        window.location.href = '/static/login.html';
        return;
    }

    // 2. Verificar "Frescura" de la sesión (Requisito: Cerrar sesión al reiniciar/refrescar)
    // Usamos sessionStorage para esta validación temporal.
    const sesionActiva = sessionStorage.getItem('session_active');

    if (sesionActiva !== 'true') {
        // Si no hay flag de sesión activa fresca (ej: por un refresh), 
        // mandamos al login para que use la opción de "Continuar con token"
        console.log("Sesión no validada recientemente. Redirigiendo a pantalla de re-ingreso...");
        window.location.href = '/static/login.html';
        return;
    }

    // 3. Limpiar el flag de sesión activa
    // Esto asegura que si el usuario REFRESCA la página, el flag ya no estará 
    // y lo mandará de vuelta al login rápido.
    sessionStorage.removeItem('session_active');
    console.log("Entrada validada. Flag de sesión limpiado para el próximo reinicio.");

    // Mostrar información del usuario
    const usuario = obtenerUsuario();
    if (usuario) {
        console.log('Usuario logueado:', usuario.nombre);
        // Mostrar el nombre en el saludo del header nuevo
        const saludoHeader = document.getElementById('saludo-header');
        if (saludoHeader) {
            saludoHeader.textContent = `¡Hola, ${usuario.nombre.split(' ')[0]}! 👋`;
        }
    }

    // Nueva lógica: Mostrar el token en la UI para fácil acceso
    // Lo ponemos ANTES de cargar los gastos para que aparezca rápido
    const tokenDisplay = document.getElementById('token-view');
    const tokenSection = document.getElementById('token-section');
    if (tokenDisplay && tokenSection) {
        console.log("Mostrando sección de token...");
        tokenDisplay.textContent = token; // El token que obtuvimos arriba
        tokenSection.style.display = 'block';
    }

    // Cargar datos al iniciar
    cargarGastos();
});

function copiarCodigoAcceso() {
    const usuario = obtenerUsuario();
    if (usuario && usuario.codigo_acceso) {
        navigator.clipboard.writeText(usuario.codigo_acceso).then(() => {
            mostrarNotificacion("📍 Código " + usuario.codigo_acceso + " copiado", "success");
        });
    } else {
        mostrarNotificacion("⚠️ No se encontró el código", "warning");
    }
}

async function editarPresupuesto() {
    const presupuesto = prompt("Ingrese el nuevo presupuesto:");
    if (presupuesto) {
        try {
            const respuesta = await fetch('/usuario/presupuesto', {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify({ nuevo_limite: parseFloat(presupuesto) })
            });
            if (respuesta.ok) {
                mostrarNotificacion("💰 Presupuesto actualizado exitosamente", "success");
                cargarGastos(); // Recargar la lista
            } else {
                mostrarNotificacion("❌ Error al actualizar el presupuesto", "error");
            }
        } catch (error) {
            console.error("Error de red:", error);
            mostrarNotificacion("❌ No se pudo conectar con el servidor", "error");
        }
    }
}

async function cargarGastos() {
    console.log("Intentando cargar gastos...");
    try {
        const filtroInput = document.getElementById('filtro-categoria')?.value;
        let url = '/gastos';

        // Si hay filtro, construir los parámetros de la URL
        if (filtroInput) {
            const categorias = filtroInput.split(',').map(c => c.trim()).filter(c => c !== "");
            const params = new URLSearchParams();
            categorias.forEach(cat => params.append('categorias', cat));
            url += `?${params.toString()}`;
        }

        // Llamamos al endpoint que devuelve la LISTA de gastos con autenticación
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        // Convertimos la respuesta a JSON
        const data = await response.json();
        console.log("Datos recibidos:", data);

        // Obtenemos referencia al cuerpo de la tabla
        const tabla = document.querySelector('#tabla-gastos');
        tabla.innerHTML = ""; // Limpiar tabla antes de agregar nuevos

        // Verificar si hay gastos
        if (data.length === 0) {
            // Mostrar mensaje amigable si no hay gastos
            const filaVacia = document.createElement('tr');
            filaVacia.innerHTML = `
                <td colspan="6" style="text-align: center; padding: 40px; color: #999;">
                    <div style="font-size: 48px; margin-bottom: 10px;">💰</div>
                    <h3 style="color: #666; margin: 10px 0;">¡Aún no tienes gastos registrados!</h3>
                    <p style="color: #999;">Empieza a ahorrar hoy mismo registrando tus gastos</p>
                </td>
            `;
            tabla.appendChild(filaVacia);
        } else {
            // Iteramos sobre los datos
            data.forEach(gasto => {
                const fila = document.createElement('tr');

                fila.innerHTML = `
                    <td style="padding: 8px; text-align: center;">${gasto.id}</td>
                    <td style="padding: 8px;">${gasto.descripcion}</td>
                    <td style="padding: 8px; font-weight: bold; color: #2E7D32;">$${gasto.monto.toFixed(2)}</td>
                    <td style="padding: 8px;">
                        <span style="background-color: #03DAC6; color: #000000; padding: 2px 8px; border-radius: 10px; font-size: 0.9em; font-weight: bold;">
                            ${gasto.categoria}
                        </span>
                    </td>
                    <td style="padding: 8px; text-align: center;">${gasto.fecha}</td>
                    <td style="text-align: center;">
                        <button onclick="eliminarGasto(${gasto.id})" style="border: none; background: none; cursor: pointer; font-size: 1.2em;">
                            🗑️
                        </button>
                    </td>
                `;

                tabla.appendChild(fila);
            });
        }

        if (filtroInput) {
            mostrarNotificacion(`Mostrando gastos de: ${filtroInput}`, 'info');
        }
    } catch (error) {
        console.error('Error al cargar gastos:', error);
        mostrarNotificacion("❌ Error al cargar los datos", "error");
    } finally {
        // Actualizamos el resumen y los gráficos secuencialmente
        await actualizarResumen();
        await renderizarGrafico();
        await renderizarGraficoComparacion();
        await renderizarGraficoDiario();
    }
}

async function eliminarGasto(id) {
    if (confirm(`¿Seguro que quieres borrar el gasto #${id}?`)) {
        try {
            const respuesta = await fetch(`/gastos/${id}`, {
                method: 'DELETE',
                headers: getAuthHeaders()
            });
            if (respuesta.ok) {
                mostrarNotificacion("🗑️ Gasto eliminado exitosamente", "success");
                cargarGastos(); // Recarga la lista automáticamente
            } else {
                mostrarNotificacion("❌ Error al eliminar el gasto", "error");
            }
        } catch (error) {
            console.error("Error de red:", error);
            mostrarNotificacion("❌ No se pudo conectar con el servidor", "error");
        }
    }
}

async function crearGasto() {
    console.log("Iniciando creación de gasto...");
    const monto = document.getElementById('monto').value;
    const descripcion = document.getElementById('descripcion').value;
    const categoria = document.getElementById('categoria').value;

    console.log("Valores leídos:", { monto, descripcion, categoria });

    if (!monto || !descripcion || !categoria) {
        mostrarNotificacion("⚠️ Por favor, complete todos los campos", "warning");
        return;
    }

    try {
        const respuesta = await fetch('/gastos', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                monto: parseFloat(monto),
                descripcion: descripcion,
                categoria: categoria
            })
        });

        if (respuesta.ok) {
            mostrarNotificacion("✅ Gasto guardado exitosamente", "success");
            cargarGastos(); // Recargar la lista
            // Limpiar formulario
            document.getElementById('monto').value = '';
            document.getElementById('descripcion').value = '';
            document.getElementById('categoria').value = '';
        } else {
            const data = await respuesta.json();
            mostrarNotificacion("❌ Error al guardar: " + data.detail, "error");
        }
    } catch (error) {
        console.error("Error de red:", error);
        mostrarNotificacion("❌ No se pudo conectar con el servidor", "error");
    }
}

/**
 * Función nueva para actualizar las tarjetas del Dashboard.
 * Se conecta al endpoint /gastos/resumen y actualiza el DOM.
 */
async function actualizarResumen() {
    try {
        console.log("🔄 Actualizando resumen...");
        const respuesta = await fetch('/gastos/resumen', {
            headers: getAuthHeaders()
        });

        if (!respuesta.ok) {
            console.error("❌ Error en respuesta:", respuesta.status);
            throw new Error("Error al obtener resumen");
        }

        // La API ahora devuelve: { 
        //   total_general, por_categoria, presupuesto_limite, 
        //   saldo_disponible, porcentaje_usado, nivel_alerta 
        // }
        const data = await respuesta.json();
        console.log("📊 Datos de resumen recibidos:", data);

        // Actualizamos las tarjetas de la nueva UI
        document.getElementById('total-gastado').innerText = `$${data.total_general.toFixed(2)}`;
        document.getElementById('balance-neto').innerText = `$${data.balance_neto.toFixed(2)}`;
        document.getElementById('valor-presupuesto').innerText = `$${data.presupuesto_limite.toFixed(2)}`;

        // Barra de progreso y texto
        const progressBar = document.getElementById('progreso-bar');
        const porcentajeTexto = document.getElementById('porcentaje-texto');
        if (progressBar && porcentajeTexto) {
            const pct = data.porcentaje_usado.toFixed(0);
            progressBar.style.width = `${pct}%`;
            porcentajeTexto.innerText = `${pct}% Usado`;

            // Color de la barra según alerta
            if (data.nivel_alerta === 'peligro') progressBar.style.background = 'var(--danger)';
            else if (data.nivel_alerta === 'advertencia') progressBar.style.background = 'var(--warning)';
            else progressBar.style.background = 'var(--primary)';
        }

        // --- SISTEMA DE ALERTA VIBRANTE ---
        const alertBar = document.getElementById('alert-system');
        if (alertBar) {
            alertBar.style.display = (data.nivel_alerta === 'peligro') ? 'flex' : 'none';
        }
    } catch (error) {
        console.error("❌ Error actualizando resumen:", error);
    }
}

let chartInstance = null;


async function exportarCSV() {
    try {
        const token = obtenerToken();
        const response = await fetch('/gastos/exportar/csv', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            // Crear un blob con el contenido CSV
            const blob = await response.blob();

            // Crear un enlace temporal para descargar
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `gastos_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();

            // Limpiar
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            mostrarNotificacion('✅ Archivo CSV descargado exitosamente', 'success');
        } else {
            mostrarNotificacion('❌ Error al exportar los datos', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarNotificacion('❌ No se pudo exportar el archivo', 'error');
    }
}

// 1. EL QUE SE BORRÓ: Gráfico Circular de Categorías
async function renderizarGrafico() {
    try {
        const respuesta = await fetch('/gastos/resumen', { headers: getAuthHeaders() });
        const data = await respuesta.json();
        if (Object.keys(data.por_categoria).length === 0) return;

        const ctx = document.getElementById('miGrafico').getContext('2d');
        if (window.chartCircular) window.chartCircular.destroy();

        window.chartCircular = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(data.por_categoria),
                datasets: [{
                    data: Object.values(data.por_categoria),
                    backgroundColor: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#F7B731', '#9B59B6']
                }]
            },
            options: { plugins: { title: { display: true, text: 'Distribución por Categoría' } } }
        });
    } catch (e) { console.error("Error circular:", e); }
}

// 2. NUEVO: Comparación Presupuesto vs Real con Semáforo
async function renderizarGraficoComparacion() {
    try {
        const respuesta = await fetch('/gastos/comparacion-presupuesto', { headers: getAuthHeaders() });
        const data = await respuesta.json();
        if (!data.categorias || data.categorias.length === 0) {
            console.log("No hay categorías para el gráfico de comparación");
            return;
        }

        // --- Lógica de Colores Dinámicos (Semáforo) ---
        const coloresDinamicos = data.gastos_reales.map((gasto, index) => {
            const presupuesto = data.presupuesto_sugerido[index];
            const ratio = gasto / presupuesto;

            if (ratio >= 1) return 'rgba(244, 67, 54, 0.8)';   // Rojo (Excedido)
            if (ratio >= 0.8) return 'rgba(255, 152, 0, 0.8)'; // Amarillo (Cerca del límite)
            return 'rgba(76, 175, 80, 0.8)';                 // Verde (Bajo control)
        });

        const bordesDinamicos = coloresDinamicos.map(color => color.replace('0.8', '1'));

        const ctx = document.getElementById('graficoComparacion').getContext('2d');
        if (window.chartBarras) window.chartBarras.destroy();

        window.chartBarras = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.categorias,
                datasets: [
                    {
                        label: 'Gasto Real',
                        data: data.gastos_reales,
                        backgroundColor: coloresDinamicos,
                        borderColor: bordesDinamicos,
                        borderWidth: 2
                    },
                    {
                        label: 'Presupuesto Sugerido',
                        data: data.presupuesto_sugerido,
                        backgroundColor: 'rgba(200, 200, 200, 0.3)',
                        borderColor: 'rgba(200, 200, 200, 0.5)',
                        borderWidth: 1,
                        type: 'line', // Lo ponemos como línea para que se vea como una meta
                        pointStyle: 'circle',
                        pointRadius: 5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' },
                    title: {
                        display: true,
                        text: 'Semáforo de Gastos vs Presupuesto',
                        font: { size: 16 }
                    }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } catch (e) { console.error("Error barras:", e); }
}

// 3. NUEVO: Gastos Día a Día
async function renderizarGraficoDiario() {
    try {
        const respuesta = await fetch('/gastos/diarios', { headers: getAuthHeaders() });
        const data = await respuesta.json();

        // Actualizar el valor acumulado del mes
        const totalAcumulado = data.totales.reduce((a, b) => a + b, 0);
        const acumuladoNode = document.getElementById('acumulado-valor');
        if (acumuladoNode) {
            acumuladoNode.innerText = `$${totalAcumulado.toFixed(2)}`;
        }
        if (!data.totales || data.totales.length === 0) return;
        // --- LÓGICA DE ACUMULACIÓN ---
        let acumulador = 0;
        const totalesAcumulados = data.totales.map(monto => {
            acumulador += monto;
            return acumulador;
        });
        const ctx = document.getElementById('graficoDiario').getContext('2d');
        if (window.chartLineas) window.chartLineas.destroy();
        window.chartLineas = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.fechas,
                datasets: [{
                    label: 'Gasto Total Acumulado ($)',
                    data: totalesAcumulados, // <--- Aquí usamos la nueva variable
                    borderColor: '#BB86FC',
                    backgroundColor: 'rgba(187, 134, 252, 0.2)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                plugins: { title: { display: true, text: 'Evolución del Gasto Mensual (Acumulado)' } }
            }
        });
    } catch (e) { console.error("Error acumulado:", e); }
}

async function filtrarTabla() {
    const texto = document.getElementById('filtro-busqueda').value.toLowerCase();
    const filas = document.querySelectorAll('#tabla-gastos tr');

    filas.forEach(fila => {
        // Obtenemos el texto de la descripción (columna 2) y categoría (columna 4)
        const descripcion = fila.cells[1]?.textContent.toLowerCase() || "";
        const categoria = fila.cells[3]?.textContent.toLowerCase() || "";

        if (descripcion.includes(texto) || categoria.includes(texto)) {
            fila.style.display = ""; // Mostrar
        } else {
            fila.style.display = "none"; // Ocultar
        }
    });
}

async function descargarPDF() {
    const token = localStorage.getItem('token');
    if (!token) return alert("Debes iniciar sesión");

    try {
        const response = await fetch('/gastos/reporte/pdf', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `reporte_finanzas_${new Date().toLocaleDateString()}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } else {
            alert("Error al generar el PDF. Verifica tu sesión.");
        }
    } catch (error) {
        console.error("Error al descargar PDF:", error);
        alert("Ocurrió un error al intentar generar el reporte.");
    }
}
