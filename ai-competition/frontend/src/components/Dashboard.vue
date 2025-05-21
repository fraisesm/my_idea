<template>
  <div class="dashboard">
    <h1>AI Competition Dashboard</h1>
    
    <div class="stats">
      <div class="stat-card">
        <h3>Teams</h3>
        <p>{{ teams.length }}</p>
      </div>
      <div class="stat-card">
        <h3>Solutions</h3>
        <p>{{ solutions.length }}</p>
      </div>
    </div>
    
    <table class="teams-table">
      <thead>
        <tr>
          <th>Team</th>
          <th v-for="task in tasks" :key="task">Task {{ task }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="team in teams" :key="team.id">
          <td>{{ team.name }}</td>
          <td v-for="task in tasks" :key="task">
            {{ getSolutionStatus(team.id, task) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: ['teams', 'solutions'],
  data() {
    return {
      tasks: Array.from({length: 50}, (_, i) => i + 1)
    }
  },
  methods: {
    getSolutionStatus(teamId, taskId) {
      const solution = this.solutions.find(s => 
        s.team_id === teamId && s.task_id === String(taskId)
      )
      return solution ? solution.status : '-'
    }
  }
}
</script>

<style>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}
.stats {
  display: flex;
  gap: 20px;
  margin: 20px 0;
}
.stat-card {
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 5px;
  min-width: 100px;
  text-align: center;
}
.teams-table {
  width: 100%;
  border-collapse: collapse;
}
.teams-table th, .teams-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
.teams-table th {
  background-color: #f2f2f2;
}
</style>