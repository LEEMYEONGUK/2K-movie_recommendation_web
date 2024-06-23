
<template>
    <div id="weekCarousel" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div v-for="(movieGroup, index) in chunkArray(store.weekMovies, 9)" :class="['carousel-item', { active: index === 0 }]" :key="index">
          <div class="d-flex">
            <WeekMovieCard v-for="movie in movieGroup" :key="movie.id" :movie="movie"/>
          </div>
        </div>
      </div>
      <div v-if="store.weekMovies.length > 9">
        <button class="carousel-control-prev" type="button" data-bs-target="#weekCarousel" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#weekCarousel" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue';
  import { useRecommendStore } from '@/stores/recommend';
  import WeekMovieCard from '@/components/WeekMovieCard.vue'
  
  const store = useRecommendStore()
  const chunkArray = (array, size) => {
  const result = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
}
    onMounted(() => {
      store.getWeekMovies()

    })
  
  </script>
  
  <style scoped>
.d-flex {
  display: flex;
}
.movie {
  padding: 5px;
  position: relative;
}

.movie:hover {
  transform: scale(1.1);
  transition: 0.3s;
  transition-delay: 0s;
}

.movie img {
  border-radius: 4px;
}

.carousel-control-prev, .carousel-control-next {
  width: 50px; /* 이미지 크기와 동일하게 설정 */
  height: 300px; /* 이미지 크기와 동일하게 설정 */
}

.carousel-control-prev-icon, .carousel-control-next-icon {
  width: 100px; /* 아이콘 크기 조정 */
  height: 100px; /* 아이콘 크기 조정 */
}

.small-carousel-button[disabled] {
  opacity: 0.5;
  pointer-events: none;
}
  </style>