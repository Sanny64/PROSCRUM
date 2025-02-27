<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
} from 'chart.js';
import type { ChartData, ChartOptions } from 'chart.js';

import type { Round } from '../types/types.ts';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

interface Props {
  roundsData: Round[];
}

const props = defineProps<Props>();

// Registriere die benötigten Chart.js-Komponenten
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale);

// Reaktives Chart-Datenobjekt
const chartData = ref<ChartData<'line'>>({
  labels: [],
  datasets: [],
});

// Funktion zur Aktualisierung der Chart-Daten
const updateChartData = () => {
  chartData.value = {
    labels: props.roundsData?.map((item) => t('output.round') + item.round_number) || [],
    datasets: [
      {
        label: t('output.from2021Chart'),
        data: props.roundsData?.map((item) => item.calc_result_2021) || [],
        borderColor: '#36A2EB',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        tension: 0.4,
      },
      {
        label: t('output.until2021Chart'),
        data: props.roundsData?.map((item) => item.calc_result_2020) || [],
        borderColor: '#FF6384',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.4,
      },
    ],
  };
};

// `watch` auf `props.roundsData`, um die Chart-Daten zu aktualisieren
watch(() => props.roundsData, updateChartData, { deep: true, immediate: true });

// Chart-Optionen
const chartOptions: ChartOptions<'line'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
    tooltip: {
      mode: 'index',
      intersect: false,
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: t('output.rounds'),
      },
    },
    y: {
      title: {
        display: true,
        text: t('output.results'),
      },
      beginAtZero: true,
    },
  },
};
</script>

<template>
  <div>
    <!-- Chart -->
    <div class="chart">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
