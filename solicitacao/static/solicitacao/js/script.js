window.onload = function() {
    /*** Cadastro de Solicitação ***/

    //Tipo de Evento Solicitado
    var tipoEventos = document.getElementsByName("tipo_evento");
    if (tipoEventos != null) {
        for (var i = 0; i < tipoEventos.length; i++)
            tipoEventos[i].addEventListener('click', exibeOpcOutro);
    }

    // Realização do Evento
    var realizacaoEvento = document.getElementsByName("evento_realizado");
    if (realizacaoEvento != null) {
        for (var i = 0; i < realizacaoEvento.length; i++)
            realizacaoEvento[i].addEventListener('click', exibeOpcsQuais);
    }

    /*** Avaliação de Solicitação ***/
    var recursos = document.getElementsByName("recursos");
    if (recursos != null) {
        for (var i = 0; i < recursos.length; i++)
            recursos[i].addEventListener('click', exibeOutroRec);
    }

    /*** Qualquer Página ***/

    //Limpa campos preenchidos em um formulário
    var btnLimpar = document.getElementById("limpar");
    if (btnLimpar  != null)
        btnLimpar.addEventListener('click', limpaCampos);

    /*** Listagem de Solicitações ***/

    // Filtro para listagem de solicitações
    var busca = document.getElementById("busca-listagem");
    if (busca != null)
        busca.onkeyup = filtro;
}

//Tipo de Evento Solicitado
function exibeOpcOutro() {
    var tipoEventos = document.getElementsByName("tipo_evento");
    var outro = document.getElementById("tipo_outro");
    var campo = document.getElementById("cam_outro");

    if (outro.checked == true) {
        campo.style.display = "block";
    }
    else {
        campo.style.display = "none";
        campo.value = "";
    }
}

//Exibe o campo para receber dados dos outros recursos
function exibeOutroRec() {
    // Opc qual
    var realizacaoEvento = document.getElementsByName("recursos");
    var outro = document.getElementById("rec_outros");
    var campo = document.getElementById("cam_outro_recurso");

    if (outro.checked == true) {
        campo.style.display = "block";
    }
    else {
        campo.style.display = "none";
        campo.value = "";
    }
}

//Para quem o evento será realizado
function exibeOpcsQuais() {
    // Opc qual
    var realizacaoEvento = document.getElementsByName("evento_realizado");
    var qual = document.getElementById("ev_qual");
    var campo = document.getElementById("cam_qual");

    // Participação Individual
    var individual = document.getElementById("ev_individual");
    var partIndividual = document.getElementById("part-indiv-opcional");
    var campo2 = document.getElementsByName("part_individual")[0];

    if (qual.checked == true) {
        campo.style.display = "block";
    }
    else {
        campo.style.display = "none";
        campo.innerHTML = "";
    }

    if (individual.checked == true) {
        partIndividual.style.display = "block";
    }
    else {
        partIndividual.style.display = "none";
        campo2.value = "";
    }
}

//Limpa campos preenchidos em um formulário
function limpaCampos() {
    var campos = document.getElementsByTagName("input");

    for (var i = 0; i < campos.length; i++) {
        switch (campos[i].type) {
            case "text":
                campos[i].value = "";
                break;
            case "date":
                campos[i].value = "";
                break;
            case "radio":
                var nome = campos[i].getAttribute("name");
                var grupo = document.getElementsByName(nome);
                grupo[0].checked = true;
                break;
            case "number":
                    campos[i].value = 1;
        }
    }

    var campoTextArea = document.getElementsByTagName("textarea");

    for (var i = 0; i < campoTextArea.length; i++) {
        campoTextArea[i].value = "";
    }
}

// Filtro para listagem de solicitações
function filtro() {
    var busca = document.getElementById("busca-listagem");
    var tabela = document.getElementById("tabela-solicitacao");
    var solicitacoes = tabela.getElementsByTagName("tr");

    // solicitacoes[0] = cabeçalho
    for (var i = 1; i < solicitacoes.length; i++) {
            var linha = solicitacoes[i].innerHTML.toLowerCase();
            var conteudo_busca = busca.value.toLowerCase();

        if (linha.match(conteudo_busca)) {
            solicitacoes[i].style.display = "";
        }
        else {
            solicitacoes[i].style.display = "none";
        }
    }
}