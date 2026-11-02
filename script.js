let peliculas = []
let generos = []

const buscador = document.getElementById("buscador")
const selectGenero = document.getElementById("selectGenero")
const contenido = document.getElementById("contenido")

async function leerCSV(archivo) {
    const respuesta = await fetch(archivo)
    const texto = await respuesta.text()
    const lineas = texto.split(/\r?\n/)
    const filas = []

    for (let i = 1; i < lineas.length; i++) {
        if (lineas[i].trim() != "") {
            const campos = lineas[i].trim().split(/,(?=(?:[^"]*"[^"]*")*[^"]*$)/)
            filas.push(campos.map(c => c.replaceAll('"', "")))
        }
    }

    return filas
}

function obtenerNombreGenero(idGenero) {
    const gen = generos.find(g => g[0] == idGenero)
    return gen ? gen[1] : "Sin género"
}

function crearFila(titulo, lista) {
    let html = `<section class="fila"><h2>${titulo} <span>(${lista.length})</span></h2><div class="fila__posters">`

    for (let p of lista) {
        // Estructura CSV: [0]id, [1]nombre, [2]id_genero, [3]resena, [4]url_poster, [5]valoracion, [6]anio, [7]baja
        const id = p[0]
        const nombre = p[1]
        const nombreGenero = obtenerNombreGenero(p[2])
        const resena = p[3]
        const poster = p[4] || `https://placehold.co/300x450/1b1b24/ffffff?text=${encodeURIComponent(nombre)}`
        const valoracion = p[5] || "S/C"
        const anio = p[6] || ""

        html += `
            <article class="movie" tabindex="0">
                <div class="movie__poster">
                    <img src="${poster}" alt="${nombre}" loading="lazy" onerror="this.src='https://placehold.co/300x450/1b1b24/ffffff?text=Sin+Portada'">
                    <span class="movie__rating">★ ${valoracion}</span>
                    <span class="movie__genre-badge">${nombreGenero}</span>
                </div>
                <div class="movie__info">
                    <div class="movie__header">
                        <h3>${nombre}</h3>
                        ${anio ? `<span class="movie__year">${anio}</span>` : ""}
                    </div>
                    <p class="movie__review">${resena}</p>
                </div>
            </article>
        `
    }

    html += `</div></section>`
    return html
}

function mostrar(lista, hayFiltro) {
    if (lista.length == 0) {
        contenido.innerHTML = "<p class='vacio'>No se encontraron películas con ese criterio.</p>"
        return
    }

    if (hayFiltro) {
        contenido.innerHTML = crearFila("Resultados de búsqueda", lista)
        return
    }

    contenido.innerHTML = crearFila("Catálogo Completo", lista)

    for (let g of generos) {
        const deEsteGenero = lista.filter(p => p[2] == g[0])
        if (deEsteGenero.length > 0) {
            contenido.innerHTML += crearFila("Películas de " + g[1], deEsteGenero)
        }
    }
}

function filtrar() {
    const texto = buscador.value.toLowerCase().trim()
    const genero = selectGenero.value
    let resultado = peliculas

    if (texto.length >= 3) {
        resultado = resultado.filter(p =>
            p[1].toLowerCase().includes(texto) ||
            p[3].toLowerCase().includes(texto)
        )
    }

    if (genero != "") {
        resultado = resultado.filter(p => p[2] == genero)
    }

    mostrar(resultado, texto.length >= 3 || genero != "")
}

async function iniciar() {
    const todosGeneros = await leerCSV("generos.csv")
    const todasPeliculas = await leerCSV("peliculas.csv")

    // Filtramos por la última columna (baja == "0")
    generos = todosGeneros.filter(g => g[g.length - 1] == "0")
    peliculas = todasPeliculas.filter(p => p[p.length - 1] == "0")

    for (let g of generos) {
        selectGenero.innerHTML += `<option value="${g[0]}">${g[1]}</option>`
    }

    mostrar(peliculas, false)
}

buscador.addEventListener("input", filtrar)
selectGenero.addEventListener("change", filtrar)

iniciar()