
<template>
  <div>
    <div v-if="store.similarMovies">
        <div class="movie-card-container">
          <div v-for="movie in paginatedStoreMovies" :key="movie.id" class="movie-card">
            <RelatedMovieCard :movie="movie" />
          </div>
        </div>
        <nav aria-label="Page navigation example" class="pagination-nav">
              <ul class="pagination justify-content-center">
                <li class="page-item px-3" :class="{ disabled: currentStorePage === 1 }">
                  <a class="page-link" href="#" @click.prevent="prevStorePage" tabindex="-1" :aria-disabled="currentStorePage === 1">Previous</a>
                </li>
                <li class="page-item px-3" v-for="page in totalStorePages" :key="page" :class="{ active: currentStorePage === page }">
                  <a class="page-link" href="#" @click.prevent="goToStorePage(page)">{{ page }}</a>
                </li>
                <li class="page-item px-3" :class="{ disabled: currentStorePage === totalStorePages }">
                  <a class="page-link" href="#" @click.prevent="nextStorePage" :aria-disabled="currentStorePage === totalStorePages">Next</a>
                </li>
              </ul>
        </nav>
      </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useMovieStore } from '@/stores/movie';
import RelatedMovieCard from './RelatedMovieCard.vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const store = useMovieStore()
const currentStorePage = ref(1);
const itemsPerStorePage = 15;
const paginatedStoreMovies = computed(() => {
  const start = (currentStorePage.value - 1) * itemsPerStorePage;
  const end = start + itemsPerStorePage;
  return store.similarMovies.slice(start, end);
});

const totalStorePages = computed(() => {
  return Math.ceil(store.similarMovies.length / itemsPerStorePage);
});

const prevStorePage = () => {
  if (currentStorePage.value > 1) currentStorePage.value--;
};

const nextStorePage = () => {
  if (currentStorePage.value < totalStorePages.value) currentStorePage.value++;
};

const goToStorePage = (page) => {
  currentStorePage.value = page;
};

onMounted(() => {
  store.getSimilar(route.params.movieId);

});
</script>

<style scoped>
.movie-card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px; /* 카드 간격을 조정합니다 */
}

.movie-card {
  width: 300px; /* 고정 너비 */
  height: 200px; /* 고정 높이 */
  margin: 10px; /* 카드 간격을 조정합니다 */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden; /* 이미지가 카드 크기를 넘지 않도록 */
}

.movie-card img {
  width: 100%; /* 이미지가 카드 너비에 맞게 조정 */
  height: 100%; /* 이미지가 카드 높이에 맞게 조정 */
  object-fit: cover; /* 이미지 비율을 유지하며 카드 크기에 맞춤 */
}

@media (max-width: 1200px) {
  .movie-card {
    width: 25%; /* 4개의 열로 조정 */
    height: auto; /* 높이를 자동으로 */
  }
}

@media (max-width: 768px) {
  .movie-card {
    width: 33.333%; /* 3개의 열로 조정 */
    height: auto; /* 높이를 자동으로 */
  }
}

@media (max-width: 480px) {
  .movie-card {
    width: 50%; /* 2개의 열로 조정 */
    height: auto; /* 높이를 자동으로 */
  }
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
