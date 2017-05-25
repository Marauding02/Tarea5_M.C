#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>


//Constante 	
float rad_mole = 1.0; //Radio de molecula en Armstrong

void savefile(float *x, float *y, int nfilas , FILE *datos );
float MINIM(int dato, float *lista);
float MAX(int dato, float *lista);

/*Main*/
int main(void)
{
    
     FILE *daticos = fopen("Canal_ionico.txt", "r");
    /*Contar el numero de lineas del archivo*/
        float cont;
	    int lineas=0;
	
	   while(!feof(daticos))
	       {
		      fscanf(daticos, "%f \n", & cont);
		      lineas++;
	       }
       return lineas;
	   fclose(daticos);

	float *x = malloc((lineas/2)*sizeof(float));
	float *y = malloc((lineas/2)*sizeof(float));
	savefile(x , y, lineas, daticos);
}


void savefile(float *x, float *y, int rows , FILE *daticos)
    {
	   int n;
	   int los_de_x;
	   int los_de_y;
	   for(n=0; n < rows ; n++)
	       {	
		      if((n%2)==0)
        	   {
			     fscanf(daticos, "%f \n", & x[los_de_x]);
        		  los_de_x++;
        	   }                            
        	   else
        	   {
        		fscanf(daticos, "%f \n", & y[los_de_y]);
			    los_de_y++;
		      }
	
	       }
	   fclose(daticos);
    }


float MAX(int dato, float *lista)
{
	int i;
	float max = lista[0];
	for(i=0; i<dato; i++)
	{
		float este_es = lista[i];
		if(este_es > max)
		{
			max = este_es;
		}
	}
	
	return max;
}

float MINIM(int dato, float *lista)
{
	int i;
	float min = lista[0];
	for(i=0; i < dato; i++)
	{
		float este_es = lista[i];
		if(este_es < min)
		{
			min = este_es;
		}
	}
		
	return min;
}

