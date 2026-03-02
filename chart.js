// ==================== Chart Configuration ====================

// Global chart configuration
const chartDefaults = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                padding: 15,
                font: {
                    size: 12,
                    weight: 'bold'
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleFont: { size: 14, weight: 'bold' },
            bodyFont: { size: 12 },
            padding: 12,
            cornerRadius: 8
        }
    }
};

// Color palette
const colorPalette = {
    primary: 'rgba(99, 102, 241, 0.8)',
    secondary: 'rgba(168, 85, 247, 0.8)',
    accent: 'rgba(59, 130, 246, 0.8)',
    success: 'rgba(34, 197, 94, 0.8)',
    warning: 'rgba(249, 115, 22, 0.8)',
    danger: 'rgba(239, 68, 68, 0.8)',
    info: 'rgba(14, 165, 233, 0.8)',
    colors: [
        'rgba(99, 102, 241, 0.8)',
        'rgba(168, 85, 247, 0.8)',
        'rgba(59, 130, 246, 0.8)',
        'rgba(34, 197, 94, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(249, 115, 22, 0.8)',
        'rgba(14, 165, 233, 0.8)',
        'rgba(236, 72, 153, 0.8)',
        'rgba(84, 82, 255, 0.8)',
        'rgba(13, 148, 136, 0.8)',
    ]
};

// ==================== Bar Chart ====================

class BarChartManager {
    constructor(canvasId, data, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.data = data;
        this.options = { ...chartDefaults, ...options };
        this.chart = null;
    }

    create(labels, values, label = 'Data') {
        if (!this.canvas) return;

        const ctx = this.canvas.getContext('2d');
        
        this.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: values,
                    backgroundColor: colorPalette.colors,
                    borderColor: colorPalette.colors.map(c => c.replace('0.8', '1')),
                    borderWidth: 2,
                    borderRadius: 8,
                    hoverBackgroundColor: colorPalette.colors.map(c => c.replace('0.8', '1'))
                }]
            },
            options: {
                ...this.options,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });

        return this.chart;
    }

    update(labels, values) {
        if (this.chart) {
            this.chart.data.labels = labels;
            this.chart.data.datasets[0].data = values;
            this.chart.update();
        }
    }

    destroy() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}

// ==================== Line Chart ====================

class LineChartManager {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = null;
    }

    create(labels, data, label = 'Data') {
        if (!this.canvas) return;

        const ctx = this.canvas.getContext('2d');

        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: colorPalette.primary,
                    backgroundColor: colorPalette.primary.replace('0.8', '0.1'),
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointBackgroundColor: colorPalette.primary,
                    pointBorderColor: 'white',
                    pointBorderWidth: 2,
                    pointHoverRadius: 7
                }]
            },
            options: {
                ...chartDefaults,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    }
                }
            }
        });

        return this.chart;
    }
}

// ==================== Pie Chart ====================

class PieChartManager {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = null;
    }

    create(labels, data, label = 'Data') {
        if (!this.canvas) return;

        const ctx = this.canvas.getContext('2d');

        this.chart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    backgroundColor: colorPalette.colors,
                    borderColor: 'white',
                    borderWidth: 2
                }]
            },
            options: {
                ...chartDefaults,
                plugins: {
                    ...chartDefaults.plugins,
                    tooltip: {
                        ...chartDefaults.plugins.tooltip,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });

        return this.chart;
    }
}

// ==================== Doughnut Chart ====================

class DoughnutChartManager {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = null;
    }

    create(labels, data, label = 'Data') {
        if (!this.canvas) return;

        const ctx = this.canvas.getContext('2d');

        this.chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    backgroundColor: colorPalette.colors,
                    borderColor: 'white',
                    borderWidth: 2
                }]
            },
            options: {
                ...chartDefaults,
                plugins: {
                    ...chartDefaults.plugins
                }
            }
        });

        return this.chart;
    }
}

// ==================== Radar Chart ====================

class RadarChartManager {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = null;
    }

    create(labels, data, label = 'Skills') {
        if (!this.canvas) return;

        const ctx = this.canvas.getContext('2d');

        this.chart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: colorPalette.primary,
                    backgroundColor: colorPalette.primary.replace('0.8', '0.2'),
                    pointBackgroundColor: colorPalette.primary,
                    pointBorderColor: 'white',
                    pointHoverBackgroundColor: 'white',
                    pointHoverBorderColor: colorPalette.primary
                }]
            },
            options: {
                ...chartDefaults,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });

        return this.chart;
    }
}

// ==================== Dashboard Chart Builder ====================

class DashboardCharts {
    constructor() {
        this.charts = {};
    }

    async loadDashboardData() {
        try {
            const response = await fetch('/api/dashboard-data');
            return await response.json();
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            return null;
        }
    }

    async initializeSkillsChart(canvasId) {
        const data = await this.loadDashboardData();
        if (!data) return;

        const barChart = new BarChartManager(canvasId);
        barChart.create(data.labels, data.data, 'Candidates with Skill');
        this.charts.skills = barChart;
    }

    async initializeTrendChart(canvasId) {
        const lineChart = new LineChartManager(canvasId);
        lineChart.create(
            ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            [5, 12, 8, 18, 25],
            'Resumes Uploaded'
        );
        this.charts.trend = lineChart;
    }

    destroyAll() {
        Object.values(this.charts).forEach(chart => {
            if (chart.destroy) chart.destroy();
        });
    }
}

// ==================== Leaderboard Chart ====================

class LeaderboardChart {
    constructor(canvasId) {
        this.canvasId = canvasId;
    }

    async create() {
        try {
            const response = await fetch('/api/leaderboard-data');
            const data = await response.json();

            const canvas = document.getElementById(this.canvasId);
            if (!canvas) return;

            const labels = data.map((item, idx) => `${idx + 1}. ${item.name}`);
            const scores = data.map(item => item.score);

            const ctx = canvas.getContext('2d');
            new Chart(ctx, {
                type: 'horizontalBar' in Chart.Chart.defaults ? 'horizontalBar' : 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Profile Score',
                        data: scores,
                        backgroundColor: colorPalette.primary,
                        borderColor: colorPalette.primary.replace('0.8', '1'),
                        borderWidth: 2
                    }]
                },
                options: {
                    ...chartDefaults,
                    indexAxis: 'y',
                    scales: {
                        x: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error creating leaderboard chart:', error);
        }
    }
}

// ==================== Initialize on Document Load ====================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize dashboard charts if on dashboard page
    if (document.getElementById('skillsChart')) {
        const dashboard = new DashboardCharts();
        dashboard.initializeSkillsChart('skillsChart');
        dashboard.initializeTrendChart('trendChart');
    }

    // Initialize leaderboard chart if on leaderboard page
    if (document.getElementById('leaderboardChart')) {
        const leaderboard = new LeaderboardChart('leaderboardChart');
        leaderboard.create();
    }
});

// Export managers globally
window.BarChartManager = BarChartManager;
window.LineChartManager = LineChartManager;
window.PieChartManager = PieChartManager;
window.DoughnutChartManager = DoughnutChartManager;
window.RadarChartManager = RadarChartManager;
window.DashboardCharts = DashboardCharts;
window.LeaderboardChart = LeaderboardChart;