document.addEventListener('DOMContentLoaded', async () => {
    const selectAluno = document.getElementById('select-aluno');
    const btnGerar = document.getElementById('btn-gerar-ia');

    // Popular combo box
    if (selectAluno) {
        try {
            const res = await fetch('/api/alunos');
            const alunos = await res.json();
            selectAluno.innerHTML = '<option value="">-- Selecione um Aluno --</option>' +
                alunos.map(a => `<option value="${a.id}">${a.nome}</option>`).join('');
        } catch (e) {
            console.error(e);
        }
    }

    // Ação ao clicar em Gerar
    if (btnGerar) {
        btnGerar.addEventListener('click', async () => {
            const id = selectAluno.value;
            if (!id) return alert('Selecione um aluno primeiro.');

            const containerParecer = document.getElementById('parecer-resultado');
            if (containerParecer) containerParecer.innerHTML = '<p>⌛ A carregar análise da IA...</p>';

            try {
                const res = await fetch(`/api/ia/parecer/${id}`);
                const data = await res.json();
                
                if (containerParecer) {
                    containerParecer.innerHTML = `
                        <div class="parecer-bloco">
                            <h4>🎯 Pontos Fortes</h4>
                            <p>${data.pontos_fortes || 'Sem dados.'}</p>
                            <h4>💡 Oportunidades de Melhoria</h4>
                            <p>${data.melhorias || 'Sem dados.'}</p>
                            <h4>📋 Recomendações</h4>
                            <p>${data.recomendacoes || 'Sem dados.'}</p>
                        </div>
                    `;
                }
            } catch (err) {
                if (containerParecer) containerParecer.innerHTML = '<p>Erro ao gerar parecer.</p>';
            }
        });
    }
});