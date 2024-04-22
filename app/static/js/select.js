const tableTels = document
  .getElementById("tabletels")
  .getElementsByTagName("tbody")[0];
const arrayTels = [];
const inputDDD = document.getElementById('ddd');
const inputTelefone = document.getElementById('telefone');
const checkWhatsapp = document.getElementById('whatsapp');
const inputTelefones = document.getElementById('telefones');
let idTel = 0;

function addTel() {
    if (arrayTels.length === 0) {
        idTel = 0
    };

    if (inputDDD == '' | inputDDD.value.length != 2 | inputDDD.value < 0) {
        const ddderro = document.getElementById('erroddd')
        ddderro.innerText = 'Valor invalido no DDD!'
        ddderro.classList.remove('hidden')
        throw console.error();
    }else{
      const ddderro = document.getElementById('erroddd')
      ddderro.classList.add('hidden')
    }

    if (inputTelefone == '' | inputTelefone.value.length < 8 | inputTelefone.value.length > 9) {
        const erroTelefone = document.getElementById('erroTelefone')
        erroTelefone.innerText = 'O telefone precisa conter de 8 a 9 numeros'
        erroTelefone.classList.remove('hidden')
        throw console.error();
    }else{
      const erroTelefone = document.getElementById('erroTelefone')
      erroTelefone.classList.add('hidden')
    }

  idTel += 1;
  var actionsTableTel =
    `<a id=${idTel} onclick="removeTel(this)"><span class="has-text-danger"><i class="fa-solid fa-trash"><span></i></a>`

  // Crie uma nova linha e colunas
  var row = tableTels.insertRow();
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);

  if (checkWhatsapp.checked == true) {
    var whatsapp = 'Sim';
  }else{
    var whatsapp = 'Não';
  }

  cell1.innerHTML = inputDDD.value;
  cell2.innerHTML = inputTelefone.value;
  cell3.innerHTML = whatsapp;
  cell4.innerHTML = actionsTableTel;

  const novoTel = {
    idFront: idTel,
    ddd: inputDDD.value,
    numero: inputTelefone.value,
    tipo: checkWhatsapp.checked,
  };

  arrayTels.push(novoTel);
  refreshInputHidden(inputTelefones);
  limparCampos([inputDDD, inputTelefone, checkWhatsapp]);
  console.log(inputTelefones.value);
}

function removeTel(elemento) {
    const idTelRemover = elemento.id;
    console.log(idTelRemover)
    var row = elemento.parentNode.parentNode;
    const index = arrayTels.findIndex(tel => tel.idFront === Number(idTelRemover));
    console.log(index)
    if (index !== -1) {
        row.parentNode.removeChild(row);
        arrayTels.splice(index, 1);
        refreshInputHidden(inputTelefones);
        if (inputTelefones.value == '[]') {
            console.log(inputTelefones.value)
            inputTelefones.value = null
        }
    }
    console.log(inputTelefones.value)
};

function limparCampos(campos) {
    for (let campo of campos) {
        try {
            campo.value = ''
            campo.checked = false
        } catch (error) {
            console.log(error)
            pass
        }
    }
}


function refreshInputHidden(campo) {
    campo.value = JSON.stringify(arrayTels);
}

function carregarTels() {
  let listTel = (JSON.parse(inputTelefones.value));
  console.log(listTel)
  listTel.forEach((tel) =>{
    console.log(tel)
    arrayTels.push(tel)
  })
  // Limpar a tabela antes de preencher novamente
  tableTels.innerHTML = '';

  // Preencher a tabela com os dados do arrayTels
  arrayTels.forEach(function(tel) {
      var actionsTableTel =
          `<a id=${tel.idFront} onclick="removeTel(this)"><span class="has-text-danger"><i class="fa-solid fa-trash"><span></i></a>`;
      var whatsapp = tel.tipo ? 'Sim' : 'Não';
      
      // Crie uma nova linha e colunas
      var row = tableTels.insertRow();
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      var cell3 = row.insertCell(2);
      var cell4 = row.insertCell(3);

      cell1.innerHTML = tel.ddd;
      cell2.innerHTML = tel.numero;
      cell3.innerHTML = whatsapp;
      cell4.innerHTML = actionsTableTel;
});
}

document.addEventListener("DOMContentLoaded", carregarTels);