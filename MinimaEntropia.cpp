#include <iostream>
#include <fstream>
#include <cassert>
#include <cmath>
#include <algorithm>
#include <cstdlib>

//Por favor compílelo así: g++ -o MinimaEntropia MinimaEntropia.cpp

void hallar_entropia(double tp_prueba, int dim_grilla[2], int N_datos, int n_as, double t_dat[], double u_dat[], double* dir);
int main(int argc, char *argv[])
{
	std::string nombre_archivo = argv[1];
	double tp_menor = atof(argv[2]);
	double tp_mayor = atof(argv[3]);
	int dimension1 = atoi(argv[4]);
	int dimension2 = atoi(argv[5]);
	int Finura = atoi(argv[6]);
	int N_as = atoi(argv[7]);
	double max_g=atof(argv[8]);
	double max_f=atof(argv[9]);
	int dimGrilla[2] = {dimension1,dimension2};
	double *dirResp = new double[3];
	std::ifstream read_file(nombre_archivo);
	assert(read_file.is_open());
	int N_filas=0;
	// Hagamos una lectura del archivo primero y anotemos la cantidad de filas que tiene con un while
	// Una vez tengamos ese número vamos a escribir lo que hay en ese archivo en las variables t, u. 
	double tk, uk, delta_uk;
	while(!read_file.eof())
	{
		read_file >> tk >> uk >> delta_uk;
		N_filas++;
	}
	N_filas--;
	// Ahora que tenemos el número de filas podemos crear unos array que sabemos que tiene una longitud de N_filas
	//std::cout << "La longitud del array es: " << N_filas <<"\n";
	// Las dos siguientes lineas es pa pedirle al read_file que vuelva a empezar desde el puro principio
	read_file.clear();
	read_file.seekg(std::ios::beg);
	// ..................::::::.....:::::....:::...:::::::::::...::::.::::..:::..:::..:::.......::::....::..
	double t[N_filas], u[N_filas];
	double delta_u; // esta linea porque read_file se confunde si no le aclaramos que son 3 columnas 
	assert(read_file.is_open());
	for (int i=0; i<N_filas; i++)
	{
		read_file >> t[i] >> u[i] >> delta_u;
		assert(read_file.good());
	}
	read_file.close();
	// Esta parte del código empieza a buscar distintos valores de entropía para cada frecuencia. 
	double f_menor, f_mayor, entropia_raw, frecuencia;
	double periodo[Finura+1], entropia[Finura+1], g[Finura+1], f[Finura+1];
	f_menor=1/tp_mayor;
	f_mayor=1/tp_menor;
	int longitud_nombreAr=nombre_archivo.length();
	std::string nombre_nuevo="Entropia_";
	for (int j=0; j<longitud_nombreAr-4; j++){ nombre_nuevo=nombre_nuevo+nombre_archivo[j];}
	nombre_nuevo=nombre_nuevo+".csv";
	std::ofstream write_output(nombre_nuevo);
	assert(write_output.is_open());
	for (int k=0; k<=Finura; k++)
	{
		frecuencia=f_menor+((f_mayor-f_menor)/Finura)*k; 
		periodo[k]=1/frecuencia;
		hallar_entropia(periodo[k],dimGrilla,N_filas,N_as,t,u, dirResp);
		entropia_raw=dirResp[0];
		g[k]=dirResp[1];
		f[k]=dirResp[2];
		if (((g[k]>max_g)||(f[k]>max_f)) && k>0)
		{
			entropia[k]=entropia[0];
		} 
		else
		{
			entropia[k]=entropia_raw;
		}
		write_output << periodo[k] << "," << entropia[k] << "," << g[k] << "," << f[k] << " \n";
		write_output.precision(10);
		assert(write_output.good());
	}
	write_output.close();
	std::cout << "Archivo "<< nombre_nuevo <<" generado" << "\n";
	delete dirResp;
	return 0;
}

/*
################################################################################################################################
:::::::::::::::::::::::::::::::::::::::::______¡¡¡¡¡ADVERTENCIA!!!!!!!_______:::::::::::::::::::::::::::::::::::::::::::::::::
###############################################################################################################################
Esta función evalua la entropía y los valores de f y g para cierto periodo de prueba
¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ ¡¡¡¡    POR FAVOR NO LA TOQUE!!!!! YA SE COMPROBÓ QUE FUNCIONA MUY BIEN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##############################################################################################################################
*/

void hallar_entropia(double tp_prueba, int dim_grilla[2], int N_datos, int n_as, double t_dat[], double u_dat[], double* dir)
{
	double phi[N_datos], xi[dim_grilla[0]];
	double inf_u, sup_u, paso_phi, paso_u, entropia, entropia_norm, xc, g, f, g_eval, f_eval, A, B, term_g, term_f;
	double *min_u, *max_u;
	int indice_i, indice_j;
	int cuenta_grilla[dim_grilla[0]][dim_grilla[1]];
	double grilla[dim_grilla[0]][dim_grilla[1]];
	for (int i=0; i<dim_grilla[0]; i++) { for (int j=0; j<dim_grilla[1]; j++) { cuenta_grilla[i][j]=0;}}
	// Aquí abajo vamos a hacer el equivalente de transformar_ts y clasificar los datos, de una, cada dato en cada una de las posiciones de la grilla
	// i es el índice que representa la cantidad de cuadros que tendrá el eje phi
	// j es el índice que represente la cantidad de cuadros que tendrá el eje u 
	// es decir dim_grilla debe colocarse así: {cuadros_phi, cuadros_u}
	A=dim_grilla[0];
	min_u=std::min_element(u_dat,u_dat+N_datos); //Esto devuelve el pointer donde está el mínimo de u
	max_u=std::max_element(u_dat,u_dat+N_datos); //Esto devuelve el pointer donde está el máximo de u
	paso_phi=1.0/dim_grilla[0]; // Ojo al operar 2 int si no ponemos 1.0 sino solo 1, c++ redondea al int mas pequeño. 
	paso_u=(*max_u-*min_u)/dim_grilla[1];
	for (int l=0; l<N_datos; l++)
	{
		phi[l]=((t_dat[l]-t_dat[0])/tp_prueba)-floor((t_dat[l]-t_dat[0])/tp_prueba);
		for (int i=0; i<dim_grilla[0]; i++)
		{
			if (phi[l]>=(i*paso_phi) && phi[l]<((i+1)*paso_phi))
			{
				indice_i=i;
			}
		}
		for (int j=0; j<dim_grilla[1]; j++)
		{
			if (u_dat[l]>=(*min_u+j*paso_u) && u_dat[l]<(*min_u+(j+1)*paso_u))
			{
				indice_j=j;
			}
		}
		cuenta_grilla[indice_i][indice_j]++;
	}
	//Ahora que tenemos la grilla en números enteros, vamos a hallar la entropía correspondiente a esa grilla
	entropia=0;
	g_eval=0;
	f_eval=0;
	for (int i=0; i<dim_grilla[0]; i++)
	{
		xi[i]=0;
		for (int j=0; j<dim_grilla[1]; j++)
		{
			if (cuenta_grilla[i][j]==0){}
			else
			{
				xc=(cuenta_grilla[i][j]+0.0)/N_datos;
				entropia=entropia+(-xc)*log(xc);
				xi[i]=xi[i]+xc;
				//Recuerda que si vas a operar dos int, tienes que agregar un +0.0 para que la respuesta te salga con decimales.
			}
		}
		term_f=pow(A, 0.5*n_as*A*A*(std::abs(xi[i]-(1.0/A))));
		if (i==0)
		{
			term_g=0.0;
		}
		else
		{
			term_g=pow(A, 0.5*n_as*A*A*(std::abs(xi[i]-xi[i-1])));
		}
		g_eval=g_eval+term_g;
		f_eval=f_eval+term_f;
	}
	f=(1/(A+1))*(log(f_eval)/log(A));
	g=(1/(A+(log(A-1)/log(A))))*(log(g_eval)/log(A));
	//std::cout<<"El valor de g es: "<<g<<" \n";
	entropia_norm=(1.0/log(dim_grilla[0]*dim_grilla[1]))*entropia;
	dir[0]=entropia_norm;
	dir[1]=g;
	dir[2]=f;
}
