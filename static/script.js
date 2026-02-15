let presenteSelecionado = null;

/* Toggle info */
document.getElementById("toggleInfo").onclick = () => {
    document.getElementById("infoBox").classList.toggle("hidden");
};

/* Carregar lista do Flask */
fetch("/api/presentes")
.then(res => res.json())
.then(data => montarLista(data));

function montarLista(lista) {
    const ul = document.getElementById("listaPresentes");

    lista.forEach(presente => {
        const li = document.createElement("li");
        li.className = "item";

        if (presente.status === 1) li.classList.add("disabled");

        li.innerHTML = `
            <img src="${presente.image}">
            <span>${presente.item}</span>
        `;

        const actions = document.createElement("div");
        actions.className = "actions";

        actions.innerHTML = `
            <button class="btn-veja">Veja</button>
            <button class="btn-dar">Dar presente</button>
        `;

        li.appendChild(actions);
        ul.appendChild(li);

        if (presente.status === 0) {
            li.addEventListener("click", () => {
                actions.classList.toggle("show");
            });

            actions.querySelector(".btn-veja").onclick = (e) => {
                e.stopPropagation();
                window.open(presente.link, "_blank");
            };

            actions.querySelector(".btn-dar").onclick = (e) => {
                e.stopPropagation();
                presenteSelecionado = presente.id;
                document.getElementById("formPopup").classList.add("show");
            };
        }
    });
}

//Fechar pop-up
function fecharPopup() {
    document.getElementById("formPopup").classList.remove("show");
}

function enviarPresente() {
    const nome = document.getElementById("nomeConvidado").value;

    fetch("/api/presentear", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ id: presenteSelecionado, nome })
    })
    .then(() => location.reload());
}
