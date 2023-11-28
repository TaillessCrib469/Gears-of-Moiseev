#include <stdio.h>
int main(){
    int count=1;
    for(int i=0; i<64; i++){
        if(i%8==0){printf("\n");count+=1;};
        if(count%2==0){
            if(i%2==0){
                printf("#");continue;
            }
            else{printf("_");continue;};
        }
        if(count%2==1){
            if(i%2==0){
                printf("_");continue;
            }
            else{printf("#");continue;};
        }
    }
}