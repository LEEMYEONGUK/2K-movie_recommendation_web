<!-- StarRating.vue -->
<template>
  <div>
    <span
      v-for="n in 5"
      :key="n"
      @click="setRating(n)"
      @mouseover="hoverRating(n)"
      @mouseleave="resetHoverRating"
      class="star fs-1"
      :class="{ filled: n <= (hoveredRating || rating) }"
    >★</span>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['update:modelValue']);

const rating = ref(props.modelValue);
const hoveredRating = ref(0);

const setRating = (value) => {
  rating.value = value;
  emit('update:modelValue', value);
};

const hoverRating = (value) => {
  hoveredRating.value = value;
};

const resetHoverRating = () => {
  hoveredRating.value = 0;
};

watch(() => props.modelValue, (newVal) => {
  rating.value = newVal;
});
</script>

<style scoped>
.star {
  cursor: pointer;
  font-size: 2rem;
  color: gray;
}
.star.filled {
  color: gold;
}
</style>