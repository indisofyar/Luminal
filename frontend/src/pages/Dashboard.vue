<template>
  <div class="p-8" v-if="transactions.length > 0">
    <div class="flex gap-4 items-center relative">
      <div class="text-xl font-bold" v-if="transactions">
        {{ transactions[0].address.name }}
      </div>
      <div class="bg-slate-800 rounded-xl p-4 relative">
        <div @click="isOpen = !isOpen">{{ transactions[0].address.address }}</div>
        <div class="p-4 bg-slate-700 top-[65px] rounded-xl absolute h-[300px]  left-0 flex flex-col" v-if="isOpen">
          <div v-for="a in addresses" class="w-full flex gap-4 hover:bg-slate-400 p-4 rounded-xl pointer"
               @click="isOpen = false; address = a.address">
            <strong> {{ a.name }} </strong> {{ a.address }}
          </div>
        </div>
      </div>
    </div>

    <section class="grid grid-cols-12 mt-8 gap-4">

      <div class="card col-span-4">
        <div class="card-title">Average Gas Fee</div>
        <div class="text-xl"> {{ avgTran }}</div>
      </div>
      <div class="card col-span-4">
        <div class="card-title">Daily active addresses</div>
        <div class="text-xl"> {{ Math.floor(Math.random() * (10000 - 8000) + 8000) }}</div>
      </div>
      <div class="card col-span-4">
        <div class="card-title">Transactions</div>
        <div class="flex w-full overflow-hidden rounded-xl text-center">
          <div
              class="bg-green-100"
              :style="{ width: ((resData.succeded_transactions / (resData.succeded_transactions + resData.failed_transactions)) * 100) + '%' }"
          >
            {{ resData.succeded_transactions }} Succeeded
          </div>
          <div
              class="bg-red-100"
              :style="{ width: ((resData.failed_transactions / (resData.succeded_transactions + resData.failed_transactions)) * 100) + '%' }"
              v-if="resData.failed_transactions > 10"
          >
            {{ resData.failed_transactions }} Failed
          </div>
        </div>
      </div>
      <div class="card h-[500px] col-span-6">
        <div class="card-title">Journey Mapping</div>
        <Bar :data="data" :options="options" class="pb-8"/>
      </div>
      <div class="card h-[500px] col-span-6">
        <div class="card-title">Fees over time</div>
        <Line :data="resData.fees_over_time_graph" :options="options" class="pb-8"/>
      </div>
    </section>
    <!--    {{transactions}}-->
  </div>
</template>

<script>

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
} from 'chart.js'
import {Bar, Line} from 'vue-chartjs'

ChartJS.register(CategoryScale, PointElement, LineElement, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  name: "Dashboard",
  components: {Bar, Line},
  data() {
    return {
      name: null,
      isOpen: false,
      address: '0x017E26DB707f62Ba3ce4641FFe2C7a109B780df1',
      addresses: [],
      loaded: false,
      transactions: [],
      avgTran: null,
      resData: null,
      options: {
        responsive: true,
        maintainAspectRatio: false
      },
      data: {
        labels: [
          'Sign Up',
          'Complete Module 1',
          'Complete Module 2',
          'Deploy Smart Contract',
        ],
        datasets: [
          {
            label: 'XRPL Data',
            backgroundColor: '#26396d',
            data: [10000, 8999, 6666, 4888]
          },
          {
            label: 'Polkadot Data',
            backgroundColor: '#e171ba',
            data: [8129, 6008, 5421, 3000]
          }
        ]
      }
    }
  },
  methods: {
    getData() {
      const vm = this;
      this.$axios.get('/api/address/' + vm.address + '/').then((res) => {
        vm.avgTran = res.data.average_gas_price
        vm.transactions = res.data.transactions
        vm.resData = res.data
      })
    },
    getAddresses() {
      const vm = this;
      this.$axios.get('/api/address/all/').then((res) => {
        vm.addresses = res.data
      })
    }
  },
  created() {
    this.getData();
    this.getAddresses();
  },

}
</script>

<style scoped>

</style>