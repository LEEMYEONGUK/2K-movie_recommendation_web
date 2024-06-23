<template>
  <div>
    <h2 class="genre-title">{{ genreName }}</h2>
    <div class="movie-card-container">
      <div v-for="movie in paginatedStoreMovies" :key="movie.id" class="movie-card">
        <GenreMovieCard :movie="movie" />
      </div>
    </div>
    <nav aria-label="Page navigation example" class="pagination-nav">
      <ul class="pagination justify-content-center">
        <li class="page-item px-3" :class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" @click.prevent="prevPage" tabindex="-1" :aria-disabled="currentPage === 1">Previous</a>
        </li>
        <li v-if="totalPages <= 10" class="page-item px-3" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
          <a class="page-link" href="#" @click.prevent="goToPage(page)">{{ page }}</a>
        </li>
        <li v-else class="page-item px-3">
          <a class="page-link" href="#">{{ currentPage }} / {{ totalPages }}</a>
        </li>
        <li class="page-item px-3" :class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" @click.prevent="nextPage" :aria-disabled="currentPage === totalPages">Next</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import GenreMovieCard from '@/components/GenreMovieCard.vue';
import { onMounted, ref, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useMovieStore } from '@/stores/movie';

const route = useRoute();
const genreId = ref(route.params.genreId);
const store = useMovieStore();
const genreName = ref('');
const currentPage = ref(1);
const itemsPerPage = 15;

watch(() => route.params.genreId, (newId) => {
  genreId.value = newId;
  currentPage.value = 1; // Reset to the first page when genre changes
  fetchMovies();
  updateGenreName();
});

const fetchMovies = () => {
  store.filterMovie(genreId.value);
};

const updateGenreName = () => {
  const genre = store.genres.find(g => g.tmdb_id === Number(genreId.value));
  genreName.value = genre ? genre.name : 'Unknown';
};

const paginatedStoreMovies = computed(() => {
  const movies = store.filteredMovies || []; // Ensure movies is an array
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return movies.slice(start, end);
});

const totalPages = computed(() => {
  const movies = store.filteredMovies || []; // Ensure movies is an array
  return Math.ceil(movies.length / itemsPerPage);
});

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const goToPage = (page) => {
  currentPage.value = page;
};

onMounted(() => {
  fetchMovies();
  updateGenreName();
});
</script>

<style scoped>
.genre-title {
  color: white;
  margin-left: 130px;
  margin-top: 70px;
}

.movie-card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center; /* 카드들을 가운데 정렬 */
  gap: 10px; /* 카드 간격을 조정합니다 */

}

.movie-card {
  height: 200px;
  width: 300px;
  gap: 3px;
  flex: 1 1 calc(16.666% - 20px); /* 6개의 열을 기본으로 합니다 */
  max-width: calc(16.666% - 20px); /* 6개의 열을 기본으로 합니다 */
  margin: 10px; /* 카드 간격을 조정합니다 */
}

@media (max-width: 1200px) {
  .movie-card {
    flex: 1 1 calc(25% - 20px); /* 4개의 열로 조정 */
    max-width: calc(25% - 20px);
  }
}

@media (max-width: 768px) {
  .movie-card {
    flex: 1 1 calc(33.333% - 20px); /* 3개의 열로 조정 */
    max-width: calc(33.333% - 20px);
  }
}

@media (max-width: 480px) {
  .movie-card {
    flex: 1 1 calc(100% - 20px); /* 2개의 열로 조정 */
    max-width: calc(50% - 20px);
  }
}

.img {
  width: 100px;
}

.pagination-nav {
  margin-top: 100px; /* 페이지 네비게이션을 30px 아래로 내립니다 */
}

.page-item.active .page-link {
  background-color: #000000; /* Bootstrap의 Danger 색상 */
  border-color: #dc3545;
  color: rgb(255, 0, 0);
}

.page-link {
  color: rgb(255, 255, 255); /* 눌리지 않았을 때 검정색 */
  background-color: black;
  border-color: black;
}
.page-item.disabled .page-link {
  background-color: #000000; /* 비활성화된 버튼의 배경색 */
  color: #6c757d; /* 비활성화된 버튼의 텍스트 색상 */
  pointer-events: none; /* 클릭 불가 */
  border-color: black;
}
</style>
