
<template>
    <div class="movie" @click="MovieDetail(movie.pk)">
    <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" class="img" alt="...">
  </div>

</template>

<script setup>
import { useRouter } from 'vue-router';
import { useMovieStore } from '@/stores/movie';
defineProps({
    movie: Object
})
const router = useRouter()
const store = useMovieStore()
const MovieDetail = function(movieId) {
  store.read_lhf(movieId)
  router.push({name:'detail', params: {movieId: movieId}})
  
}
</script>

<style scoped>
.img {
  width: 180px;
  height: 300px; /* 이미지 높이 추가 */
}

</style>





