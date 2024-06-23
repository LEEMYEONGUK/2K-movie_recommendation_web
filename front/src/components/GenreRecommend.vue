
<template>
  <div>
    
    <div class="movie-card-container">
      <div v-for="(movieGroup, index) in chunkArray( movies['movies'], 9)" :class="['carousel-item', { active: index === 0 }]" :key="index">
        <div class="d-flex">
            <GenreRecMovieCard v-for="movie in movieGroup" :key="movie.id" :movie="movie"/>
          </div>
            </div>

    </div>
  </div>
</template>

<script setup>
import GenreRecMovieCard from '@/components/GenreRecMovieCard.vue';
const props = defineProps({
  movies:Object
})
console.log(props.movies)
const chunkArray = (array, size) => {
  const result = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
}

</script>

<style scoped>
.date-carousel {
  padding: 20px;
}
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