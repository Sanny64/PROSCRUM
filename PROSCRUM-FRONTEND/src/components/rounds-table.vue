<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from "vue";
import type { Round } from "../types/types.ts";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

interface Props {
  roundsData: Round[];
}

const props = defineProps<Props>();

const showMore = ref(false);
const maxVisibleRows = ref(5); // Standardwert

// Funktion zur Berechnung der Zeilen basierend auf Bildschirmgröße
const updateMaxVisibleRows = () => {
  const screenHeight = window.innerHeight;

  // Beispiel: 60px pro Zeile + 100px für Header/Padding
  maxVisibleRows.value = Math.floor((screenHeight - 450) / 60);
};

// `computed`-Property, um die Anzahl der sichtbaren Zeilen zu begrenzen
const displayedRounds = computed(() => {
  const maxRows = showMore.value ? props.roundsData.length : maxVisibleRows.value;
  return props.roundsData.slice().reverse().slice(0, maxRows);
});

// Event-Listener für Bildschirmgrößenänderungen
onMounted(() => {
  updateMaxVisibleRows();
  window.addEventListener("resize", updateMaxVisibleRows);
});

onUnmounted(() => {
  window.removeEventListener("resize", updateMaxVisibleRows);
});

</script>

<template>
  <div class="tableDiv">
    <table style="width: 100%;">
      <thead>
      <tr>
        <th>{{ t('output.round') }}</th>
        <th>{{ t('output.resultsFrom2021') }}</th>
        <th>{{ t('output.resultsUntil2020') }}</th>
        <th>{{ t('output.scoreDifferential') }}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(item, index) in displayedRounds" :key="item.round_number" >
        <td>{{ item.round_number }}</td>
        <td>{{ item.calc_result_2021 }}</td>
        <td>{{ item.calc_result_2020 }}</td>
        <td>{{ item.score_differential }}</td>
      </tr>
      <!-- Mehr/Weniger Button -->
      <tr v-if="props.roundsData.length > maxVisibleRows && !showMore" @click="showMore = true" class="more-row">
        <td colspan="4" style="text-align: center; cursor: pointer; font-weight: bold;">
          {{ t('output.more') }}
        </td>
      </tr>
      <tr v-if="showMore" @click="showMore = false" class="more-row">
        <td colspan="4" style="text-align: center; cursor: pointer; font-weight: bold;">
          {{ t('output.fewer') }}
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>


<style scoped>

@import "../style/rounds-table.css";


</style>
