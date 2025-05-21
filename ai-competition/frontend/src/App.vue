<template>
  <div id="app">
    <Dashboard :teams="teams" :solutions="solutions" />
  </div>
</template>

<script>
import Dashboard from './components/Dashboard.vue'

export default {
  name: 'App',
  components: {
    Dashboard
  },
  data() {
    return {
      teams: [],
      solutions: []
    }
  },
  async mounted() {
    const response = await fetch('http://localhost:8000/dashboard')
    const data = await response.json()
    this.teams = data.teams
    this.solutions = data.solutions
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  margin: 20px;
}
</style>