<template>
  <div class="genres container">
    <div v-for="genre in genres" :key="genre.tmdb_id" class="genre-item">
      <button
        type="button"
        class="btn btn-outline-danger"
        :class="{ active: selectedGenreId === genre.tmdb_id }"
        @click="onGenreClick(genre.tmdb_id)"
      >
        {{ genre.name }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useMovieStore } from '@/stores/movie';

const router = useRouter();
const route = useRoute(); 
const store = useMovieStore();
const genres = store.genres;
const selectedGenreId = ref(null);

const onGenreClick = (genreId) => {
  if (selectedGenreId.value === genreId) {
    selectedGenreId.value = null;
    router.push({ name: 'list' });
  } else {
    selectedGenreId.value = genreId;
    router.push({ name: 'genre', params: { genreId } });
  }
};

watch(() => route.params.genreId, (newGenreId) => {
  if (newGenreId) {
    selectedGenreId.value = Number(newGenreId);
  } else {
    selectedGenreId.value = null; 
  }
});

onMounted(() => {
  if (route.params.genreId) {
    selectedGenreId.value = Number(route.params.genreId);
  }
});
</script>

<style scoped>
button {
  width: 110px;
}

.genres {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  grid-template-columns: repeat(10, 1fr);
}

@media (min-width: 1200px) {
  .genres {
    grid-template-columns: repeat(7, 1fr); 
  }
}

@media (min-width: 992px) and (max-width: 1199px) {
  .genres {
    grid-template-columns: repeat(5, 1fr); 
  }
}

@media (min-width: 768px) and (max-width: 991px) {
  .genres {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 767px) {
  .genres {
    grid-template-columns: repeat(2, 1fr); 
  }
}


button.active {
  background-color: #dc3545;
  color: white;
}
</style>
