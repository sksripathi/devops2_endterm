const animateCounters = () => {
  const counters = document.querySelectorAll('.counter');

  counters.forEach((counter) => {
    const target = Number(counter.dataset.target || 0);
    const decimals = Number(counter.dataset.decimals || 0);
    const duration = 1000;
    const startTime = performance.now();

    const step = (currentTime) => {
      const progress = Math.min((currentTime - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = target * eased;
      counter.textContent = value.toFixed(decimals);

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        counter.textContent = target.toFixed(decimals);
      }
    };

    requestAnimationFrame(step);
  });
};

const renderCharts = (data) => {
  const sharedOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 1200,
      easing: 'easeOutQuart',
    },
    plugins: {
      legend: {
        labels: {
          color: '#f4f7fb',
        },
      },
    },
  };

  const occupationCtx = document.getElementById('occupationChart');
  if (occupationCtx) {
    new Chart(occupationCtx, {
      type: 'pie',
      data: {
        labels: data.occupation_labels,
        datasets: [{
          data: data.occupation_counts,
          backgroundColor: ['#4fa8ff', '#2f6ee2', '#73d2de', '#95f5d5', '#ffd166', '#ff6b6b', '#9b5de5', '#f15bb5'],
          borderColor: '#030816',
          borderWidth: 2,
        }],
      },
      options: sharedOptions,
    });
  }

  const ageCtx = document.getElementById('ageChart');
  if (ageCtx) {
    new Chart(ageCtx, {
      type: 'bar',
      data: {
        labels: data.age_labels,
        datasets: [{
          label: 'Users',
          data: data.age_counts,
          backgroundColor: ['#4fa8ff', '#2f6ee2', '#4fa8ff', '#2f6ee2', '#4fa8ff', '#2f6ee2'],
          borderRadius: 8,
        }],
      },
      options: {
        ...sharedOptions,
        scales: {
          y: {
            beginAtZero: true,
            ticks: { color: '#f4f7fb' },
            grid: { color: 'rgba(255,255,255,0.08)' },
          },
          x: {
            ticks: { color: '#f4f7fb' },
            grid: { display: false },
          },
        },
      },
    });
  }

  const genderCtx = document.getElementById('genderChart');
  if (genderCtx) {
    new Chart(genderCtx, {
      type: 'doughnut',
      data: {
        labels: data.gender_labels,
        datasets: [{
          data: data.gender_counts,
          backgroundColor: ['#4fa8ff', '#ff6b6b'],
          borderColor: '#030816',
          borderWidth: 2,
        }],
      },
      options: sharedOptions,
    });
  }
};

document.addEventListener('DOMContentLoaded', () => {
  animateCounters();
  if (window.dashboardData) {
    renderCharts(window.dashboardData);
  }
});
