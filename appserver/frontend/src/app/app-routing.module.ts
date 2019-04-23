import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SimpleDatasetEdaComponent } from './simple-dataset-eda/simple-dataset-eda.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const routes: Routes = [
    { path: 'eda/:wfid',      
      component: SimpleDatasetEdaComponent 
    },
    { path: '',
      redirectTo: 'eda',
      pathMatch: 'full'
    },
    { path: '**', component: PageNotFoundComponent }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
