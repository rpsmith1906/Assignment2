#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

int main (int argc, char *argv[] )
{
     char *misspelled[1000] ;
     FILE *fp ;
     int i ;
     int mswords=0 ;
     node* cnode ;
     node* nnode ;

     hashmap_t hashtable[HASH_SIZE] ;


     if ( argc < 3 ) 
     {
          printf("Usage %s <input file> < word list >...\n", argv[0] ) ;
          return (1) ;
     }

     if (( fp = fopen(argv[1], "r")) == NULL )
     {
          printf ( "Error! could not open file \n" ) ;
          return (1) ;
     }

     if ( load_dictionary( argv[2], hashtable ) == true )
     {
          mswords=check_words(fp, hashtable, misspelled) ;
     }

     fclose (fp) ;

     for ( i=0; i<HASH_SIZE; i++ )
     {
          if ( hashtable[i] == NULL ) { continue ; }

          cnode = hashtable[i] ;
          while ( cnode != NULL )
          {
               nnode = cnode->next ;
               free ( cnode ) ;
               cnode = nnode ;
          }
     }

     if ( mswords > 0 ) 
     { 
          if ( mswords == 1 ) { printf("There was %i misspelled words found.\n\n", mswords ) ; }
          else { printf("There were %i misspelled words found.\n\n", mswords ) ; }

          for ( i=0; i<mswords; i++ )
          {
               printf ("%s\n", misspelled[i] );
               free ( misspelled[i] ) ;
          }
     }
}
