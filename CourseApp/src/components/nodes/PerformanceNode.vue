<template>
  <component :is="nodeComponent" :config="config" :key="nodeType" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import NeuralCore from './NeuralCore.vue'
import CyberGrid from './CyberGrid.vue'
import PulseWave from './PulseWave.vue'
import DataPrism from './DataPrism.vue'
import ParticleVortex from './ParticleVortex.vue'
import HolographicHUD from './HolographicHUD.vue'
import FractalDNA from './FractalDNA.vue'
import AuroraFluid from './AuroraFluid.vue'
import FloatingNodes from './FloatingNodes.vue'
import QuantumOrbit from './QuantumOrbit.vue'

const props = defineProps<{
  nodeType: string
  config?: Record<string, any>
}>()

const nodeMap: Record<string, any> = {
  'neural-core': NeuralCore,
  'cyber-grid': CyberGrid,
  'pulse-wave': PulseWave,
  'data-prism': DataPrism,
  'particle-vortex': ParticleVortex,
  'holographic-hud': HolographicHUD,
  'fractal-dna': FractalDNA,
  'aurora-fluid': AuroraFluid,
  'floating-nodes': FloatingNodes,
  'quantum-orbit': QuantumOrbit
}

const nodeComponent = computed(() => {
  return nodeMap[props.nodeType] || NeuralCore
})
</script>
