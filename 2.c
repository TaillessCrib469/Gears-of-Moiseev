#include <stdio.h>
#include <math.h>
int main(){
    int a=0;
    int b=0;
    int c=0;


    printf("a=");
    scanf("%d",&a);
    printf("b=");
    scanf("%d",&b);
    printf("c=");
    scanf("%d",&c);
    double d=b*b-4*a*c;
    if(d<0){
        printf("Решений нет");
        return 0;
    }
    if(d==0){
        d=-b/(2*a);
        printf("Ваш корешок: %f",d);
        return 0;
    }
    double x1=(-b+sqrt(d))/(2*a);
    double x2=(-b-sqrt(d))/(2*a);
    printf("Ваши хорни: %f; %f",x1, x2);
    return 0;
}