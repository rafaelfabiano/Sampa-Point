document.addEventListener('DOMContentLoaded', function () {
	// Passando as preferências como JSON do backend para o frontend
	const scores = JSON.parse(document.getElementById('user-preferences-data').textContent);

	// Função para criar o gráfico de radar
	const labels = Object.keys(scores).map(function (key) {
		return key.charAt(0).toUpperCase() + key.slice(1);  // Convertendo para a primeira letra maiúscula
	});

	const data = Object.values(scores);  // Obtendo os valores das preferências

	const maxValue = Math.max(...data);  // Descobrindo o valor máximo para ajustar a escala

	const ctx = document.getElementById('radarChart').getContext('2d');
	const radarChart = new Chart(ctx, {
		type: 'radar',
		data: {
			labels: labels,
			datasets: [{
				label: 'User Preferences',
				data: data,
				backgroundColor: 'rgba(255, 99, 132, 0.2)',
				borderColor: 'rgba(255, 99, 132, 1)',
				borderWidth: 1,
				pointBackgroundColor: 'rgba(255, 99, 132, 1)',
			}]
		},
		options: {
			scale: {
				ticks: {
					beginAtZero: true,
					max: maxValue + (maxValue * 0.2)  // Adiciona uma margem de 20% ao valor máximo
				}
			}
		}
	});
});
