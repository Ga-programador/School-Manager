document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/dashboard/metrics');
        if (!response.ok) return;
        const data = await response.json();

        // Cards Superiores
        if(document.getElementById('total-alunos')) document.getElementById('total-alunos').textContent = data.total_alunos || 0;
        if(document.getElementById('media-frequencia')) document.getElementById('media-frequencia').textContent = (data.media_frequencia || 0) + '%';
        if(document.getElementById('alunos-risco')) document.getElementById('alunos-risco').textContent = data.alunos_risco || 0;
        if(document.getElementById('turmas-ativas')) document.getElementById('turmas-ativas').textContent = data.turmas_ativas || 0;

        // Renderizar Tabela de Alunos em Risco
        const tabelaRisco = document.getElementById('tabela-risco-body');
        if (tabelaRisco && data.alunos_criticos) {
            tabelaRisco.innerHTML = data.alunos_criticos.map(aluno => `
                <tr>
                    <td>${aluno.nome}</td>
                    <td>${aluno.turma}</td>
                    <td>${aluno.media}</td>
                    <td>${aluno.frequencia}%</td>
                    <td><span class="badge ${aluno.status_class}">${aluno.status}</span></td>
                    <td><button class="btn-ia-sm" onclick="gerarParecer(${aluno.id})">✨ Gerar Parecer IA</button></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Erro ao carregar dashboard:', err);
    }
});