#include "psbbv/applications/catalogue.h"
#include <assert.h>
#include <stdio.h>
int main(void) {
    psbbv_app_catalogue c; const psbbv_app_record *r; char id[10]; size_t i;
    psbbv_app_catalogue_init(&c);
    assert(psbbv_app_catalogue_add(&c,"VPHB00001","VitaPluginHub","0.2.1")==PSBBV_APP_OK);
    assert(psbbv_app_catalogue_add(&c,"VPHB00001","Duplicate","1")==PSBBV_APP_DUPLICATE);
    assert(psbbv_app_catalogue_add(&c,"bad-id","Bad","1")==PSBBV_APP_INVALID);
    r=psbbv_app_catalogue_find(&c,"VPHB00001"); assert(r && r->title[0]=='V');
    for(i=1;i<PSBBV_APP_CATALOGUE_CAPACITY;i++){(void)snprintf(id,sizeof(id),"A%08zu",i);assert(psbbv_app_catalogue_add(&c,id,"Fixture","1")==PSBBV_APP_OK);}
    assert(psbbv_app_catalogue_add(&c,"OVERFLOW1","Overflow","1")==PSBBV_APP_FULL);
    puts("PSBBV application catalogue tests passed"); return 0;
}
