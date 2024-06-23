
<template>
  <div  @click="MovieDetail(movie.tmdb_id)">
    <div id="box">
    <img :src="`https://image.tmdb.org/t/p/w500${movie.backdrop_path}`" class="img" alt="...">
    <div class="overlay">
      <h1 class="heading">{{ movie.title }}</h1>
  </div>
  </div>
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
  store.movieDetail(movieId)
  router.push({name:'detail', params: {movieId: movieId}})
  
}

</script>

<style scoped>
#box {
  width: 100%; /* 부모 컨테이너의 너비를 가득 채움 */
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  margin: 0; /* 여백을 제거하여 부모 컨테이너에 맞춤 */
  transition: all 0.3s cubic-bezier(0.42, 0.0, 0.58, 1.0);
  position: relative; /* overlay 위치 설정을 위해 추가 */
}

#box:hover {
  box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
  transform: translateY(-10px);
}

#box .img {
  display: block;
  width: 100%; /* 이미지가 박스의 너비에 맞춰지도록 */
  height: 100%;
}

#box .heading {
  font-size: 18px;
  color: white;
  font-weight: bolder;
}

#box .texts {
  font-size: 14px;
  line-height: 18px;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}

#box:hover .overlay {
  opacity: 1;
  pointer-events: auto;
}

p i {
  color: yellow;
}

</style>




