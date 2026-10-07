function abrirModal() {
  document.getElementById('modal-aluno').classList.remove('hidden');
}

function fecharModal() {
  document.getElementById('modal-aluno').classList.add('hidden');
  document.getElementById('form-aluno').reset();
}

async function carregarAlunos() {
  try {
    const res = await fetch('/alunos');
    const alunos = await res.json();
    const tbody = document.getElementById('tabela-alunos');
    tbody.innerHTML = '';

    if (alunos.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:#94a3b8;">Nenhum aluno cadastrado.</td></tr>`;
      return;
    }

    alunos.forEach(aluno => {
      tbody.innerHTML += `
        <tr>
          <td>#${aluno.id}</td>
          <td><strong>${aluno.nome}</strong></td>
          <td>${aluno.email}</td>
          <td>
            <button onclick="deletarAluno(${aluno.id})" style="color:#ef4444; background:none; border:none; cursor:pointer; font-weight:600;">Excluir</button>
          </td>
        </tr>
      `;
    });
  } catch (err) {
    console.error("Erro ao carregar alunos:", err);
  }
}

async function salvarAluno(event) {
  event.preventDefault();
  const nome = document.getElementById('nome').value;
  const email = document.getElementById('email').value;

  try {
    const res = await fetch('/alunos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome, email })
    });

    if (res.ok) {
      fecharModal();
      carregarAlunos();
    }
  } catch (err) {
    alert("Erro ao salvar aluno.");
  }
}

async function deletarAluno(id) {
  if (confirm("Deseja realmente remover este aluno?")) {
    await fetch(`/alunos/${id}`, { method: 'DELETE' });
    carregarAlunos();
  }
}

// Inicializa a listagem ao abrir a tela
carregarAlunos();