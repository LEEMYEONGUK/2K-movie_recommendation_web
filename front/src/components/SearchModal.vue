<template>
  <div>
    <input v-model="query" @input="searchMovies" placeholder="Search for a movie" class="search-input"/>
    <div v-if="movies.length">
      <div class="movie-card-container">
        <div v-for="movie in movies" :key="movie.tmdb_id" class="movie-card" @click="selectMovie(movie.title, movie.tmdb_id)">
            <div class="movie-image-container">
              <img class="img" :src="`https://image.tmdb.org/t/p/w1280${movie.backdrop_path}`" alt="...">
              <p class="movie-title">{{ movie.title }}</p>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { defineProps } from 'vue'

const props = defineProps(['closeModal'])
const query = ref('')
const movies = ref([])
const router = useRouter()

const searchMovies = async () => {
  if (query.value.length >= 1) {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/search/', {
        params: {
          query: query.value,
        }
      })
      movies.value = response.data.results
    } catch (error) {
      console.error('영화 정보를 가져오는 중 오류 발생:', error)
    }
  } else {
    movies.value = []
  }
}

const selectMovie = (title, movieId) => {
  query.value = title
  router.push({ name: 'detail', params: { movieId: movieId } })
  props.closeModal()
}
</script>

<style scoped>
.search-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f0f0f0; /* 회색 배경색 */
}
.search-input:focus {
    outline: 2px solid rgb(255, 0, 0);
}

.img {
  width: 100%;
  height: auto;
  display: block;
}

.search-result__card:hover {
  cursor: pointer;
  color: white;
  background-color: #3b82f6;
}

.movie-card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px; /* 카드 간격을 조정합니다 */
}

.movie-card {
  flex: 1 1 calc(33.333% - 20px); /* 3개의 열로 조정 */
  max-width: calc(33.333% - 20px);
  margin: 10px; /* 카드 간격을 조정합니다 */
}

.movie-image-container {
  position: relative;
}

.movie-title {
  position: absolute;
  bottom: 10px;
  left: 10px;
  color: white;
  background-color: rgba(0, 0, 0, 0.5); /* 반투명 검정 배경 */
  padding: 5px;
  border-radius: 5px;
  font-size: 14px;
  margin: 0; /* 기본 여백 제거 */
}
</style>
