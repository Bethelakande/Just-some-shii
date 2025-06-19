import { useState } from 'react'
import ClerkProviderWithRoutes from './auth/ClerkProviderWithRoutes'
import './App.css'
import {Routes, Route} from "react-router-dom"
import {Layout} from "./layout/Layout"
import {AuthenticationPage} from "./auth/Authenticationpage"
import {ChallengeGenerator} from "./Challenge/ChallengeGenerator"
import {MCQChallenge} from "./Challenge/MCQChallenge"
import {HistoryPanel} from "./history/HistoryPanel"

function App() {
   return <ClerkProviderWithRoutes>
      <Routes>
         <Route path='/sign-in/*' element={<AuthenticationPage/>}></Route>
         <Route path='/sign-up' element={<AuthenticationPage/>}></Route>
         <Route element={<Layout />}>
            <Route path='/' element={<ChallengeGenerator></ChallengeGenerator>}></Route>
            <Route path='/history' element={<HistoryPanel></HistoryPanel>}></Route>
         </Route>
    </Routes>
   </ClerkProviderWithRoutes>
   
}

export default App
