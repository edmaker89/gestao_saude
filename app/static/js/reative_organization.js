
document.addEventListener("DOMContentLoaded", async () => {
  const organizacaoSelect = document.getElementById("organizacao");
  const estabelecimentoSelect = document.getElementById("estabelecimento");
  const departamentoSelect = document.getElementById("departamento");
  const colaboradorSelect = document.getElementById("colaborador")

  // Obtém os valores dos campos hidden
  try {
    const selectedColaborador = document.getElementById("id_colaborador").value
  }catch {
    const selectedColaborador = ''
  }
  try {
    const selectedOrganizacao = document.getElementById("id_organizacao").value;
    const selectedEstabelecimento = document.getElementById("id_estabelecimento").value;
    const selectedDepartamento = document.getElementById("id_departamento").value;
    // Define o valor de organização e carrega as opções correspondentes
    if (organizacaoSelect && selectedOrganizacao) {
      console.log('entrou no if 1')
      organizacaoSelect.value = selectedOrganizacao;
      await handleOrganizacaoChange(selectedEstabelecimento, selectedDepartamento);
      estabelecimentoSelect.value = selectedEstabelecimento;
      if (estabelecimentoSelect) {
        console.log('entrou no if 2')
        await handleEstabelecimentoChange();
        departamentoSelect.value = selectedDepartamento
        if (departamentoSelect) {
          await handleDepartamentoChange();
          colaboradorSelect.value = selectedColaborador
        }
      }
    }else if (estabelecimentoSelect && selectedEstabelecimento){
        estabelecimentoSelect.value = selectedEstabelecimento;
        await handleEstabelecimentoChange();
        departamentoSelect.value = selectedDepartamento
        if (departamentoSelect) {
          await handleDepartamentoChange();
          colaboradorSelect.value = selectedColaborador
        }
      }else if (departamentoSelect && selectedDepartamento) {
        departamentoSelect.value = selectedDepartamento
        await handleDepartamentoChange();
          colaboradorSelect.value = selectedColaborador
      }
  } catch {
    const selectedOrganizacao = '';
    const selectedEstabelecimento = '';
    const selectedDepartamento = '';
  }

  // Adiciona event listeners para mudanças nos selects
  if (organizacaoSelect) {
      organizacaoSelect.addEventListener("change", () => handleOrganizacaoChange());
  }

  if (estabelecimentoSelect) {
      estabelecimentoSelect.addEventListener("change", () => handleEstabelecimentoChange());
  }
});

// Função para lidar com a seleção de uma organização
async function handleOrganizacaoChange(selectedEstabelecimento = null, selectedDepartamento = null) {
  const organizacaoId = document.getElementById("organizacao").value;
  const estabelecimentoSelect = document.getElementById("estabelecimento");
  const departamentoSelect = document.getElementById("departamento");

  if (organizacaoId) {
      try {
          const estabelecimentos = await fetchEstabelecimentos(organizacaoId);
          populateSelect(estabelecimentoSelect, estabelecimentos, 'Selecione um estabelecimento', selectedEstabelecimento);
          clearSelect(departamentoSelect, 'Selecione um departamento');
          
          // Carrega os departamentos automaticamente se um estabelecimento foi passado
          if (selectedEstabelecimento) {
              await handleEstabelecimentoChange(selectedDepartamento);
          }
      } catch (error) {
          console.error("Erro ao buscar estabelecimentos:", error);
      }
  } else {
      clearSelect(estabelecimentoSelect, 'Selecione um estabelecimento');
      clearSelect(departamentoSelect, 'Selecione um departamento');
  }
}

// Função para lidar com a seleção de um estabelecimento
async function handleEstabelecimentoChange(selectedDepartamento = null) {
  const estabelecimentoId = document.getElementById("estabelecimento").value;
  const departamentoSelect = document.getElementById("departamento");

  if (estabelecimentoId) {
      try {
          const departamentos = await fetchDepartamentos(estabelecimentoId);
          populateSelect(departamentoSelect, departamentos, 'Selecione um departamento', selectedDepartamento);
      } catch (error) {
          console.error("Erro ao buscar departamentos:", error);
      }
  } else {
      clearSelect(departamentoSelect, 'Selecione um departamento');
  }
}

// Função para lidar com a seleção de um Departamentp
async function handleDepartamentoChange(selectedColaborador = null) {
  const departamentoId = document.getElementById("estabelecimento").value;
  const colaboradorSelect = document.getElementById("colaborador");

  if (departamentoId) {
      try {
          const colaboradores = await fetchColaboradores(departamentoId);
          populateSelectColaborador(colaboradorSelect, colaboradores, 'Selecione um colaborador', selectedColaborador);
      } catch (error) {
          console.error("Erro ao buscar colaboradores:", error);
      }
  } else {
      clearSelect(colaboradorSelect, 'Selecione um colaborador');
  }
}


// Função para buscar estabelecimentos pela organização
async function fetchEstabelecimentos(organizacaoId) {
  const response = await fetch(`/organization/api/organizacao/${organizacaoId}/estabelecimentos`);
  return response.json();
}

// Função para buscar departamentos pelo estabelecimento
async function fetchDepartamentos(estabelecimentoId) {
  const response = await fetch(`/organization/api/estabelecimento/${estabelecimentoId}/departamentos`);
  return response.json();
}

// Função para buscar colaboradores pelo departamento
async function fetchColaboradores(departamentoId) {
  const response = await fetch(`/organization/api/departamento/${departamentoId}/colaboradores`);
  return response.json();
}

// Função para preencher o select com as opções e definir o valor selecionado
function populateSelect(selectElement, items, placeholderText, selectedValue = null) {
  clearSelect(selectElement, placeholderText);
  items.forEach(item => {
      const option = document.createElement("option");
      option.value = item['id'];
      option.textContent = item['nome'];
      if (selectedValue && item['id'] === selectedValue) {
          option.selected = true;
      }
      selectElement.appendChild(option);
  });
}

function populateSelectColaborador(selectElement, items, placeholderText, selectedValue = null) {
  clearSelect(selectElement, placeholderText);
  items.forEach(item => {
      const option = document.createElement("option");
      option.value = item['id'];
      option.textContent = item['nome_completto'];
      if (selectedValue && item['id'] === selectedValue) {
          option.selected = true;
      }
      selectElement.appendChild(option);
  });
}

// Função para limpar o select e adicionar a opção inicial
function clearSelect(selectElement, placeholderText) {
  selectElement.innerHTML = `<option value=''>${placeholderText}</option>`;
}