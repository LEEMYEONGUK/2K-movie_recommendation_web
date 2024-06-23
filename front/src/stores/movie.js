import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
export const useMovieStore = defineStore('movie', () => {
  const userStore = useUserStore()

  const genres = ref([])
  const movies = ref([])
  const filteredMovies = ref([])
 
  const movie = ref({})
  const movieVideoKey = ref('')
  const likesCount = ref(0)
  const hatesCount = ref(0)
  const favorited = ref(false)
  const liked = ref(false)
  const hated = ref(false)
  const similarMovies = ref([])
  const favoriteMovies = ref([])
  const ACCESS_TOKEN = process.env.VUE_APP_ACCESS_TOKEN
  const getGenres = function() {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/movies/genres'
    })
    .then((res) => {

      genres.value = res.data
    })
  }

  const getMovies = function() {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/movies/'
    })
    .then((res) => {

      movies.value = res.data
    })
  }

  const filterMovie = function(genreId) {
    filteredMovies.value = null
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/filter-genre/${genreId}/`
    })
    .then((res) => {

      filteredMovies.value = res.data
    })
  }


  const movieDetail = function (movieId) {
    let options = {
        method: 'GET',
        url: `https://api.themoviedb.org/3/movie/${movieId}`,
        params: {language: 'ko-KR'},
        headers: {
            accept: 'application/json',
            Authorization: `Bearer ${ACCESS_TOKEN}`
        }
    };

    axios
    .request(options)
    .then(function (response) {
        movieVideoKey.value = ''
        movie.value = response.data

        return movie.value.id
    })
    .then(function (movieId) {
        axios
      .request({
          method: 'GET',
          url: `https://api.themoviedb.org/3/movie/${movieId}/videos`,
          params: {language: 'en-US'},
          headers: {
              accept: 'application/json',
              Authorization: `Bearer ${ACCESS_TOKEN}`
          }
      })
      .then(function (response) {
          const videoObj = response.data.results.find((obj) => obj.type === "Trailer")

          movieVideoKey.value = videoObj.key
          console.log(movieVideoKey.value)
      })
    })
    .catch(function (error) {
        console.error(error);
    });
  }

  const read_lhf = function(movieId) {
    axios.get(`http://127.0.0.1:8000/api/v1/movies/${movieId}/${userStore.userId}/`)
      .then((res) => {
        liked.value = res.data.liked
        hated.value = res.data.hated
        favorited.value = res.data.favorited
        likesCount.value = res.data.like_count
        hatesCount.value = res.data.hate_count
      })
      .catch((error) => {
        console.error(error)
      })
  }
  
  const likeMovie = function(movieId) {
    axios.post(`http://127.0.0.1:8000/api/v1/movies/${movieId}/likes/${userStore.userId}/`, null, {
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {
        liked.value = res.data.liked
        likesCount.value = res.data.count
      })
      .catch((error) => {
        console.error(error)
      })
  }

  const hateMovie = function(movieId) {
    axios.post(`http://127.0.0.1:8000/api/v1/movies/${movieId}/hates/${userStore.userId}/`, null, {
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {

        hated.value = res.data.hated
        hatesCount.value = res.data.count
      })
      .catch((error) => {
        console.error(error)
      })
  }

  const favoriteMovie = function(movieId) {
    axios.post(`http://127.0.0.1:8000/api/v1/movies/${movieId}/favorite/${userStore.userId}/`, null, {
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) => {
        favorited.value = res.data.favorited
      })
      .catch((error) => {
        console.error(error)
      })
  }
  const getSimilar = (movieId) => {
    axios({
      method: 'GET',
      url: `http://127.0.0.1:8000/api/v1/movies/${movieId}/related/`,
    })
    .then((res) => {
          similarMovies.value = res.data
          console.log(res.data)

        })
  }
  const myFavoriteMovie = function() {
    axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/v1/movies/${userStore.userId}/my_favorite/`,
        headers: {
          Authorization: `Token ${userStore.token}`
        }
      }).then((response) => {

        favoriteMovies.value = response.data
        console.log("프로필 찜한 영화 조회")
      })
        .catch((error) => {
          console.log(error)
      })
  }
  return {  
    genres,
    getGenres,
    movies,
    getMovies,
    filterMovie,
    filteredMovies,
    movieDetail,
    movie,
    movieVideoKey,
    liked,
    hated,
    favorited,
    likeMovie,
    hateMovie,
    favoriteMovie,
    read_lhf,
    likesCount,
    hatesCount,
    getSimilar,
    similarMovies,
    myFavoriteMovie,
    favoriteMovies
  }
}, { persist: true })
